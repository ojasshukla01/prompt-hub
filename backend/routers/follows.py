from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user
from models import Follow, User
from schemas import FollowResponse
from uuid import UUID

router = APIRouter(
    prefix="/follows",
    tags=["Follows"]
)

@router.post("/{user_id}", response_model=FollowResponse)
def follow_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if user_id == current_user.id:
        raise HTTPException(status_code=400, detail="You cannot follow yourself.")

    # Check if already following
    existing = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already following this user.")

    follow = Follow(
        follower_id=current_user.id,
        following_id=user_id
    )
    db.add(follow)
    db.commit()
    db.refresh(follow)
    return follow

@router.delete("/{user_id}")
def unfollow_user(user_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    follow = db.query(Follow).filter(
        Follow.follower_id == current_user.id,
        Follow.following_id == user_id
    ).first()
    if not follow:
        raise HTTPException(status_code=404, detail="You are not following this user.")
    db.delete(follow)
    db.commit()
    return {"message": "Unfollowed successfully."}

@router.get("/followers/{user_id}", response_model=list[FollowResponse])
def get_followers(user_id: UUID, db: Session = Depends(get_db)):
    followers = db.query(Follow).filter(Follow.following_id == user_id).all()
    return followers

@router.get("/following/{user_id}", response_model=list[FollowResponse])
def get_following(user_id: UUID, db: Session = Depends(get_db)):
    following = db.query(Follow).filter(Follow.follower_id == user_id).all()
    return following
