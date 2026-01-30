# seed_db.py
from app.database import Base, engine, SessionLocal
from app.models import User
from app.core.security import hash_password
import os

# Ensure DB tables exist
Base.metadata.create_all(bind=engine)

# Create uploads folder if needed
os.makedirs("uploads", exist_ok=True)

def seed():
    db = SessionLocal()
    try:
        # Check if TestUser already exists
        existing_user = db.query(User).filter(User.email == "test@daolytics.local").first()
        if not existing_user:
            test_user = User(
                username="TestUser",
                email="test@daolytics.local",
                hashed_password=hash_password("password123")
            )
            db.add(test_user)
            db.commit()
            print("✅ TestUser created")
        else:
            print("ℹ️ TestUser already exists")
    finally:
        db.close()

if __name__ == "__main__":
    seed()

