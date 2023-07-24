from typing import Union, Optional

from pydantic import BaseModel


class ReviewCreate(BaseModel):
    text: str
    grade: int
    pros: Optional[str]
    cons: Optional[str]


class ReviewRead(ReviewCreate):
    pass


class CommentCreate(BaseModel):
    text: str
