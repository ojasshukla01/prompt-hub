from pydantic import BaseModel, EmailStr
from typing import List, Optional
import uuid
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    role: str

    class Config:
        from_attributes = True

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

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class FollowResponse(BaseModel):
    id: UUID
    follower_id: UUID
    following_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
        
class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: UUID
    content: str
    author_id: UUID
    prompt_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True


class LikeResponse(BaseModel):
    id: UUID
    user_id: UUID
    prompt_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True
