import sys
import random
sys.path.append('.')

from app.db import session, models
from app.core import security

def seed():
    print("Recreating database...")
    models.Base.metadata.drop_all(bind=session.engine)
    models.Base.metadata.create_all(bind=session.engine)
    
    db = session.SessionLocal()
    
    print("Adding Admin user...")
    admin = models.User(
        id="admin_123",
        email="admin@parksmart.test",
        name="ParkSmart Admin",
        hashed_password=security.get_password_hash("admin123"),
        is_active=True
    )
    db.add(admin)
    db.commit()
    
    print("Adding ParkSmart Main Lot...")
    lot = models.ParkingLot(name="ParkSmart Main", admin_id="admin_123")
    db.add(lot)
    db.commit()
    db.refresh(lot)
    
    print("Seeding exactly 48 slots (3 Zones of 16)...")
    statuses = ["free", "free", "free", "occupied", "occupied", "reserved"]
    for i in range(48):
        zone = "A" if i < 16 else "B" if i < 32 else "C"
        num = (i % 16) + 1
        name = f"{zone}{num:02d}"
        rate = 50.0 if zone == "C" else 75.0 if zone == "A" else 100.0
        
        slot = models.Slot(
            lot_id=lot.id,
            name=name,
            rate_per_hour=rate,
            status=random.choice(statuses)
        )
        db.add(slot)
    
    db.commit()
    db.close()
    print("Database seeded successfully with 48 slots!")

if __name__ == "__main__":
    seed()
