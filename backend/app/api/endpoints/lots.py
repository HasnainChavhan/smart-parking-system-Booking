from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from app.db import models, session
from app.schemas import schemas
from app.api.endpoints.websockets import manager

router = APIRouter()

@router.get("/", response_model=List[schemas.ParkingLot])
def read_parking_lots(skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    # Auto-release expired slots
    now = datetime.now()
    expired_bookings = db.query(models.Booking).filter(
        models.Booking.status == "paid",
        models.Booking.end_time <= now
    ).all()
    
    if expired_bookings:
        for b in expired_bookings:
            b.status = "completed"
            if b.slot and b.slot.status != "free":
                b.slot.status = "free"
        db.commit()

    lots = db.query(models.ParkingLot).offset(skip).limit(limit).all()
    return lots

@router.post("/", response_model=schemas.ParkingLot)
def create_parking_lot(lot: schemas.ParkingLotCreate, db: Session = Depends(session.get_db)):
    db_lot = models.ParkingLot(**lot.dict(), admin_id="test_admin")
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

@router.post("/{lot_id}/slots", response_model=schemas.Slot)
def create_slot(lot_id: int, slot: schemas.SlotCreate, db: Session = Depends(session.get_db)):
    db_slot = models.Slot(**slot.dict(), lot_id=lot_id)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.post("/{lot_id}/slots/{slot_id}/status", response_model=schemas.Slot)
async def update_slot_status(
    lot_id: int, 
    slot_id: int, 
    status_update: schemas.SlotStatusUpdate, 
    db: Session = Depends(session.get_db)
):
    slot = db.query(models.Slot).filter(models.Slot.id == slot_id, models.Slot.lot_id == lot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    current_status = slot.status

    # --- Priority Logic ---
    # 1. If Slot is 'reserved'
    if current_status == "reserved":
        # Only allow switching to 'occupied' (Car arrived)
        # Identify if ML is saying 'free' -> Ignore
        if status_update.status == "free":
            print(f"Ignored ML update 'free' for Reserved slot {slot_id}")
            return slot # Return current state without change

    slot.status = status_update.status
    db.commit()
    db.refresh(slot)

    # Broadcast to WS
    message = {
        "type": "slot_update",
        "slot": {
            "id": slot.id,
            "status": slot.status,
            "lot_id": lot_id
        }
    }
    await manager.broadcast(message, str(lot_id))
    
    return slot

@router.post("/{lot_id}/clear_slots")
async def clear_all_slots(lot_id: int, db: Session = Depends(session.get_db)):
    slots = db.query(models.Slot).filter(models.Slot.lot_id == lot_id).all()
    if not slots:
        raise HTTPException(status_code=404, detail="No slots found for this lot")
    
    for slot in slots:
        slot.status = "free"
        # Broadcast each update using the websocket manager
        message = {
            "type": "slot_update",
            "slot": {
                "id": slot.id,
                "status": "free",
                "lot_id": lot_id
            }
        }
        await manager.broadcast(message, str(lot_id))

    slot_ids = [s.id for s in slots]
    if slot_ids:
        bookings = db.query(models.Booking).filter(
            models.Booking.slot_id.in_(slot_ids),
            models.Booking.status == "paid"
        ).all()
        for b in bookings:
            b.status = "cancelled_by_admin"

    db.commit()
    return {"message": "All slots cleared successfully"}

@router.get("/{lot_id}/revenue")
def get_total_revenue(lot_id: int, db: Session = Depends(session.get_db)):
    bookings = db.query(models.Booking).join(models.Slot).filter(
        models.Slot.lot_id == lot_id,
        models.Booking.status == "paid"
    ).all()
    total = sum(b.amount for b in bookings if b.amount)
    total = round(total, 2)
    return {"revenue": total}
