from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from models import User
from utils import verify_password, create_access_token
from database import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/token")
def login_for_access_token(
    db: Session = Depends(get_db),
    username: str = Form(...),
    password: str = Form(...)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
