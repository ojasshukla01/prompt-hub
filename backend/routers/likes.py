from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models import Like, Prompt, User
import uuid

router = APIRouter(
    prefix="/likes",
    tags=["Likes"]
)

@router.post("/{prompt_id}/like")
def like_prompt(prompt_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found.")
    like = Like(user_id=current_user.id, prompt_id=prompt_id)
    db.add(like)
    db.commit()
    return {"message": "Prompt liked!"}

@router.post("/{prompt_id}/unlike")
def unlike_prompt(prompt_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    like = db.query(Like).filter(Like.user_id == current_user.id, Like.prompt_id == prompt_id).first()
    if like:
        db.delete(like)
        db.commit()
        return {"message": "Prompt unliked."}
    raise HTTPException(status_code=404, detail="Like not found.")