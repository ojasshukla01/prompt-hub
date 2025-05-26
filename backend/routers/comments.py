from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comment, Prompt, User
from typing import List
from pydantic import BaseModel
import uuid
from dependencies import get_current_active_admin_user

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
        orm_mode = True

@router.get("/prompt/{prompt_id}", response_model=List[CommentResponse])
def get_comments(prompt_id: uuid.UUID, db: Session = Depends(get_db)):
    comments = db.query(Comment).filter(Comment.prompt_id == prompt_id).all()
    return comments

@router.post("/", response_model=CommentResponse)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    # In real implementation, get author_id from auth
    author_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    db_comment = Comment(
        prompt_id=comment.prompt_id,
        content=comment.content,
        author_id=author_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

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