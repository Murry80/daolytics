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
        # List of test users to seed
        users_to_add = [
            ("TestUser", "test@daolytics.local", "password123"),
            ("Alice", "alice@daolytics.local", "alice123"),
            ("Bob", "bob@daolytics.local", "bob123"),
        ]

        for username, email, password in users_to_add:
            existing_user = db.query(User).filter(User.email == email).first()
            if not existing_user:
                db.add(User(
                    username=username,
                    email=email,
                    hashed_password=hash_password(password)
                ))
                print(f"✅ Created user: {username}")
            else:
                print(f"ℹ️ User already exists: {username}")

        db.commit()

        # Print total users in DB for verification
        user_count = db.query(User).count()
        print(f"ℹ️ Total users in DB: {user_count}")

    finally:
        db.close()

if __name__ == "__main__":
    seed()

