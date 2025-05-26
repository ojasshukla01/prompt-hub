from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Follow, User
from typing import List
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix="/follows",
    tags=["Follows"]
)

class FollowResponse(BaseModel):
    id: uuid.UUID
    follower_id: uuid.UUID
    following_id: uuid.UUID

    class Config:
        orm_mode = True

@router.post("/{user_id}")
def follow_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    # Placeholder: current user id
    follower_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    follow = Follow(follower_id=follower_id, following_id=user_id)
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

@router.delete("/{user_id}")
def unfollow_user(user_id: uuid.UUID, db: Session = Depends(get_db)):
    follower_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.following_id == user_id
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="Not following user")
    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed"}
