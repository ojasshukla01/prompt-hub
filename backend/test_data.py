from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from utils import hash_password
import uuid

db: Session = SessionLocal()

existing_user = db.query(User).filter_by(username="testuser").first()
if not existing_user:
    new_user = User(
        id=uuid.uuid4(),
        username="testuser",
        email="test@example.com",
        hashed_password=hash_password("testpassword"),
        profile_picture=None,
        bio=None,
        role="admin"
    )
    db.add(new_user)
    db.commit()
else:
    print("User already exists. Skipping insertion.")

db.close()
