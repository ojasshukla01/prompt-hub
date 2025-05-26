from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import User
from utils import verify_password, create_access_token, hash_password
from pydantic import BaseModel
from dependencies import get_current_user, get_current_active_admin_user
from typing import List
import uuid
import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# --- Request/Response Schemas ---
class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    is_active: bool

    class Config:
        orm_mode = True

# --- Login Endpoint ---
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(db_user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

# --- Create User Endpoint ---
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login", response_model=schemas.TokenResponse)
def login_user(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == form_data.email).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_profile(profile: schemas.UserCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    current_user.username = profile.username or current_user.username
    current_user.bio = profile.bio or current_user.bio
    current_user.profile_picture = profile.profile_picture or current_user.profile_picture
    db.commit()
    db.refresh(current_user)
    return current_user

# Admin-only route
@router.get("/admin/check")
def check_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admins only!")
    return {"message": "You are an admin!"}

# GET ALL USERS (ADMIN ONLY)
@router.get("/", response_model=List[UserResponse])
def get_all_users(db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_admin_user)):
    users = db.query(User).all()
    return users

# UPDATE USER (ADMIN ONLY)
@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: uuid.UUID, user_data: UserCreate, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_admin_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db_user.username = user_data.username
    db_user.email = user_data.email
    db_user.role = user_data.role
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE USER (ADMIN ONLY)
@router.delete("/{user_id}")
def delete_user(user_id: uuid.UUID, db: Session = Depends(get_db),
                 current_user: User = Depends(get_current_active_admin_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}