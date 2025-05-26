from sqlalchemy import Column, String, Text, Enum, ForeignKey, DateTime, func, Table, Boolean
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
import enum
import uuid
from pydantic import BaseModel
from database import Base
from datetime import datetime

class VisibilityEnum(enum.Enum):
    public = "public"
    private = "private"

class LoginRequest(BaseModel):
    username: str
    password: str

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    profile_picture = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    role = Column(String, default="user")  # 👈 role field
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    prompts = relationship("Prompt", back_populates="author")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")
    followers_associations = relationship("Follow", back_populates="following_user", foreign_keys="Follow.following_id")
    following_associations = relationship("Follow", back_populates="follower_user", foreign_keys="Follow.follower_id")

    followers = relationship("User",
                             secondary="follows",
                             primaryjoin="User.id==Follow.following_id",
                             secondaryjoin="User.id==Follow.follower_id",
                             viewonly=True)

    following = relationship("User",
                             secondary="follows",
                             primaryjoin="User.id==Follow.follower_id",
                             secondaryjoin="User.id==Follow.following_id",
                             viewonly=True)
    
class Prompt(Base):
    __tablename__ = "prompts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(ARRAY(String))
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.public)
    version_history = Column(JSONB, default=[])
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    author = relationship("User", back_populates="prompts")
    comments = relationship("Comment", back_populates="prompt", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="prompt", cascade="all, delete-orphan")


class Follow(Base):
    __tablename__ = "follows"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    follower_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    following_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    follower_user = relationship("User", back_populates="following_associations", foreign_keys=[follower_id])
    following_user = relationship("User", back_populates="followers_associations", foreign_keys=[following_id])


class Comment(Base):
    __tablename__ = "comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)

    author = relationship("User", back_populates="comments")
    prompt = relationship("Prompt", back_populates="comments")



class Like(Base):
    __tablename__ = "likes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    prompt_id = Column(UUID(as_uuid=True), ForeignKey("prompts.id"), nullable=False)

    user = relationship("User", back_populates="likes")
    prompt = relationship("Prompt", back_populates="likes")

