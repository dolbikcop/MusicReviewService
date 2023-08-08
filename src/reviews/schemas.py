import datetime
from typing import Union, Optional, List

from pydantic import BaseModel

from src.reviews.enums import ReactionType


class ReviewCreate(BaseModel):
    text: str
    grade: int
    pros: Optional[str]
    cons: Optional[str]


class CommentCreate(BaseModel):
    text: str


class CommentRead(CommentCreate):
    id: int
    owner_id: int
    likes: int
    dislikes: int
    created_at: datetime.datetime


class ReviewRead(ReviewCreate):
    id: int
    likes: int
    dislikes: int
    comments: List[CommentRead]
    created_at: datetime.datetime


class ReactionCreate(BaseModel):
    reaction_type: ReactionType
    content_id: int
