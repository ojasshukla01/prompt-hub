from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_db, get_current_user
from models import Follow, User
from schemas import FollowResponse
from uuid import UUID
import uuid

router = APIRouter(
    prefix="/follows",
    tags=["Follows"]
)


@router.post("/{user_id}/follow")
def follow_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_to_follow = db.query(User).filter(User.id == user_id).first()
    if not user_to_follow:
        raise HTTPException(status_code=404, detail="User not found.")
    follow = Follow(follower_id=current_user.id, following_id=user_id)
    db.add(follow)
    db.commit()
    return {"message": f"Now following {user_to_follow.username}"}

@router.post("/{user_id}/unfollow")
def unfollow_user(user_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow = db.query(Follow).filter(Follow.follower_id == current_user.id, Follow.following_id == user_id).first()
    if follow:
        db.delete(follow)
        db.commit()
        return {"message": "Unfollowed."}
    raise HTTPException(status_code=404, detail="Not following this user.")

@router.get("/followers/{user_id}", response_model=list[FollowResponse])
def get_followers(user_id: UUID, db: Session = Depends(get_db)):
    followers = db.query(Follow).filter(Follow.following_id == user_id).all()
    return followers

@router.get("/following/{user_id}", response_model=list[FollowResponse])
def get_following(user_id: UUID, db: Session = Depends(get_db)):
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    return following
