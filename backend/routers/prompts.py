from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Prompt, User
from typing import List
from pydantic import BaseModel
import uuid

router = APIRouter(
    prefix="/prompts",
    tags=["Prompts"]
)

class PromptCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    visibility: str = "public"

class PromptResponse(BaseModel):
    id: uuid.UUID
    title: str
    content: str
    tags: List[str]
    visibility: str
    author_id: uuid.UUID

    class Config:
        orm_mode = True

@router.get("/", response_model=List[PromptResponse])
def get_prompts(db: Session = Depends(get_db)):
    prompts = db.query(Prompt).all()
    return prompts

@router.post("/", response_model=PromptResponse)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db)):
    # For now, assume user_id is a placeholder (later use auth)
    user_id = uuid.UUID("11111111-1111-1111-1111-111111111111")
    db_prompt = Prompt(
        title=prompt.title,
        content=prompt.content,
        tags=prompt.tags,
        visibility=prompt.visibility,
        author_id=user_id
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt
