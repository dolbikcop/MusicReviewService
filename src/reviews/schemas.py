import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    text: str
    grade: int = Field(gt=0, le=5)
    pros: Optional[str] = None
    cons: Optional[str] = None


class CommentCreate(BaseModel):
    text: str


class CommentRead(CommentCreate):
    id: int
    owner_id: str
    likes: int
    dislikes: int
    created_at: datetime.datetime


class ReviewRead(ReviewCreate):
    id: int
    owner_id: str
    likes: int
    dislikes: int
    created_at: datetime.datetime
