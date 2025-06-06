from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comment, Prompt, User
from typing import List
from pydantic import BaseModel
import uuid
from uuid import UUID
from models import Comment, Like, Prompt, User
from schemas import CommentCreate, CommentResponse, LikeResponse
from dependencies import get_current_active_admin_user, get_current_user

router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

class CommentCreate(BaseModel):
    prompt_id: uuid.UUID
    content: str

class CommentResponse(BaseModel):
    id: uuid.UUID
    prompt_id: uuid.UUID
    content: str
    author_id: uuid.UUID

    class Config:
        from_attributes = True

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prompt = db.query(Prompt).filter(Prompt.id == comment.prompt_id).first()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found.")
    new_comment = Comment(content=comment.content, prompt_id=prompt.id, author_id=current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@router.get("/prompt/{prompt_id}", response_model=list[CommentResponse])
def get_comments(prompt_id: str, db: Session = Depends(get_db)):
    return db.query(Comment).filter(Comment.prompt_id == prompt_id).all()

# Example: Adding admin delete for comments
@router.delete("/{comment_id}")
def delete_comment(comment_id: uuid.UUID, db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_admin_user)):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted"}

@router.post("/like/{prompt_id}", response_model=LikeResponse)
def like_prompt(prompt_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # Prevent duplicate likes
    existing_like = db.query(Like).filter(Like.user_id == current_user.id, Like.prompt_id == prompt_id).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="You already liked this prompt.")
    like = Like(user_id=current_user.id, prompt_id=prompt_id)
    db.add(like)
    db.commit()
    db.refresh(like)
    return like

@router.delete("/like/{prompt_id}")
def unlike_prompt(prompt_id: UUID, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    like = db.query(Like).filter(Like.user_id == current_user.id, Like.prompt_id == prompt_id).first()
    if not like:
        raise HTTPException(status_code=404, detail="You haven't liked this prompt.")
    db.delete(like)
    db.commit()
    return {"message": "Unliked successfully."}