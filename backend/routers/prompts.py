from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Prompt, User
from typing import List
from pydantic import BaseModel
import uuid
from dependencies import get_current_user, get_current_active_admin_user
import schemas

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
        from_attributes = True

@router.get("/", response_model=List[schemas.PromptResponse])
def get_prompts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    prompts = db.query(Prompt).offset(skip).limit(limit).all()
    return prompts

@router.post("/", response_model=PromptResponse)
def create_prompt(prompt: PromptCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_prompt = Prompt(
        title=prompt.title,
        content=prompt.content,
        tags=prompt.tags,
        visibility=prompt.visibility,
        author_id=current_user.id
    )
    db.add(db_prompt)
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

# UPDATE UPDATE PROMPT TO USE ADMIN
@router.put("/{prompt_id}")
def update_prompt(prompt_id: uuid.UUID, prompt: PromptCreate, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_admin_user)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db_prompt.title = prompt.title
    db_prompt.content = prompt.content
    db_prompt.tags = prompt.tags
    db_prompt.visibility = prompt.visibility
    db.commit()
    db.refresh(db_prompt)
    return db_prompt

# UPDATE DELETE PROMPT TO USE ADMIN
@router.delete("/{prompt_id}")
def delete_prompt(prompt_id: uuid.UUID, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_active_admin_user)):
    db_prompt = db.query(Prompt).filter(Prompt.id == prompt_id).first()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    db.delete(db_prompt)
    db.commit()
    return {"message": "Prompt deleted"}
