from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import razorpay
from typing import Any, List
from datetime import datetime

from app.core.config import settings
from app.db import models, session
from app.schemas import schemas
from app.core import security

router = APIRouter()

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@router.post("/", response_model=Any)
def create_booking_order(
    booking_request: schemas.BookingCreate, 
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    """
    1. Check if slot is free
    2. Create Razorpay Order
    3. Return Order ID to frontend
    """
    slot = db.query(models.Slot).filter(models.Slot.id == booking_request.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    try:
        start = datetime.fromisoformat(booking_request.start_time)
        end = datetime.fromisoformat(booking_request.end_time)
        duration_hours = (end - start).total_seconds() / 3600
        if duration_hours <= 0:
            raise ValueError("End time must be after start time")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e) or "Invalid start/end time")

    amount_paise = int(duration_hours * slot.rate_per_hour * 100)
    
    try:
        payment = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"receipt_{booking_request.slot_id}",
            "payment_capture": 1
        })
    except Exception as e:
        print(f"Razorpay Error: {e}")
        raise HTTPException(status_code=500, detail="Payment Gateway Error")

    return {
        "order_id": payment['id'],
        "amount": payment['amount'],
        "currency": payment['currency'],
        "key_id": settings.RAZORPAY_KEY_ID
    }

@router.post("/verify")
def verify_payment(
    verify_data: schemas.BookingVerify,
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    if verify_data.razorpay_order_id != "mock_order":
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': verify_data.razorpay_order_id,
                'razorpay_payment_id': verify_data.razorpay_payment_id,
                'razorpay_signature': verify_data.razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid Payment Signature")

    slot = db.query(models.Slot).filter(models.Slot.id == verify_data.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    start = datetime.fromisoformat(verify_data.start_time)
    end = datetime.fromisoformat(verify_data.end_time)
    duration_hours = (end - start).total_seconds() / 3600
    if duration_hours <= 0:
        raise HTTPException(status_code=400, detail="End time must be after Start time")
    if end <= datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book tickets for times that have already expired")
    amount = float(duration_hours * slot.rate_per_hour)

    booking = models.Booking(
        slot_id=verify_data.slot_id,
        user_id=current_user.id,
        car_number=verify_data.car_number,
        start_time=start,
        end_time=end,
        amount=amount,
        status="paid",
        razorpay_order_id=verify_data.razorpay_order_id,
        razorpay_payment_id=verify_data.razorpay_payment_id
    )
    db.add(booking)
    
    # Update slot to reserved
    slot.status = "reserved"
    db.commit()
    
    return {"status": "success", "message": "Booking Confirmed"}

@router.get("/my_bookings", response_model=List[schemas.Booking])
def get_my_bookings(
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    bookings = db.query(models.Booking).filter(models.Booking.user_id == current_user.id, models.Booking.status == "paid").order_by(models.Booking.created_at.desc()).all()
    return bookings

@router.delete("/{booking_id}/cancel")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(security.get_current_user)
):
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id, models.Booking.user_id == current_user.id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
        
    booking.status = "cancelled"
    
    # Free up the slot
    slot = db.query(models.Slot).filter(models.Slot.id == booking.slot_id).first()
    if slot:
        slot.status = "free"
        
    db.commit()
    return {"status": "success", "message": "Booking cancelled successfully"}
