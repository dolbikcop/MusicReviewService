from typing import Optional, List

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..auth.models import User

from ..database import Base


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True, nullable=False)

    text: Mapped[str] = mapped_column(String(500), nullable=False)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))
    review = relationship('Review', foreign_keys=[review_id])


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True, nullable=False)
    album_id: Mapped[int] = mapped_column(String, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    text: Mapped[str] = mapped_column(String(500), nullable=True)
    pros: Mapped[str] = mapped_column(String(250), nullable=True)
    cons: Mapped[str] = mapped_column(String(250), nullable=True)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    comments_id: Mapped[Optional[List[int]]] = mapped_column(ForeignKey(Comment.id))
    comments = relationship('Comment', foreign_keys=[comments_id], collection_class=set, cascade='all,delete')
