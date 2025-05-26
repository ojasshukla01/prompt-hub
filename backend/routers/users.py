from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from typing import List
from pydantic import BaseModel, EmailStr
import uuid
from utils import hash_password  # Use hashing!
from utils import verify_password, create_access_token
from fastapi import status
from dependencies import get_current_user
import schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

class UserLogin(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pwd = hash_password(user.password)
    db_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        bio=user.bio,
        profile_picture=user.profile_picture,
        hashed_password=hashed_pwd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == login_request.username).first()
    
    if not user or not verify_password(login_request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {"access_token": access_token, "token_type": "bearer"}

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