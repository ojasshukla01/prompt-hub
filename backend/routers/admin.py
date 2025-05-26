from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from dependencies import get_current_active_admin_user
import uuid

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/users/")
def list_all_users(db: Session = Depends(get_db), admin_user: User = Depends(get_current_active_admin_user)):
    return db.query(User).all()

@router.delete("/users/{user_id}")
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db), admin_user: User = Depends(get_current_active_admin_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully."}

@router.get("/admin-only-data")
def admin_data(current_user: User = Depends(get_current_active_admin_user)):
    return {"message": "Only admins can see this!"}