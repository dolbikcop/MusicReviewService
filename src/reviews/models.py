from datetime import datetime
from sqlalchemy import Integer, ForeignKey, String, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import ReactionType
from ..auth.models import User

from ..database import Base


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey('user.id'), index=True, nullable=False)
    album_id: Mapped[int] = mapped_column(String, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    text: Mapped[str] = mapped_column(String(500), nullable=True)
    pros: Mapped[str] = mapped_column(String(250), nullable=True)
    cons: Mapped[str] = mapped_column(String(250), nullable=True)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    comments = relationship('Comment', backref='review', cascade='all, delete-orphan')
    reactions = relationship('ReviewReaction', backref='review')


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[str] = mapped_column(ForeignKey(User.id), index=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    text: Mapped[str] = mapped_column(String(500), nullable=False)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'), nullable=False)

    reactions = relationship('CommentReaction', backref='comment')


class ReviewReaction(Base):
    __tablename__ = 'review_reaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reaction_type: Mapped[int] = mapped_column(Enum(ReactionType), index=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    review_id: Mapped[int] = mapped_column(ForeignKey(Review.id), nullable=False)


class CommentReaction(Base):
    __tablename__ = 'comment_reaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reaction_type: Mapped[int] = mapped_column(Enum(ReactionType), index=True)

    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)
    comment_id: Mapped[int] = mapped_column(ForeignKey(Comment.id), nullable=False)

