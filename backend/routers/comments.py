from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Comment, Prompt
from typing import List
from pydantic import BaseModel
import uuid

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
