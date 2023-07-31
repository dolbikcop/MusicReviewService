from sqlalchemy import Integer, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .enums import ReactionType
from ..auth.models import User

from ..database import Base


class Review(Base):
    __tablename__ = 'review'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'), index=True, nullable=False)
    album_id: Mapped[int] = mapped_column(String, nullable=False)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)

    text: Mapped[str] = mapped_column(String(500), nullable=True)
    pros: Mapped[str] = mapped_column(String(250), nullable=True)
    cons: Mapped[str] = mapped_column(String(250), nullable=True)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    owner = relationship('User', back_populates="reviews", lazy='subquery')
    comments = relationship('Comment', collection_class=set, cascade='all, delete-orphan')
    reactions = relationship('ReviewReaction', back_populates='review', cascade='all, delete-orphan')


class Comment(Base):
    __tablename__ = 'comment'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey(User.id), index=True, nullable=False)

    text: Mapped[str] = mapped_column(String(500), nullable=False)

    likes: Mapped[int] = mapped_column(Integer, default=0)
    dislikes: Mapped[int] = mapped_column(Integer, default=0)

    review_id: Mapped[int] = mapped_column(ForeignKey('review.id'))

    owner = relationship('User', back_populates="comments", lazy='subquery')
    review = relationship('Review', foreign_keys=[review_id], back_populates='comments')
    reactions = relationship('CommentReaction', back_populates='comment', cascade='all, delete-orphan')


class ReviewReaction(Base):
    __tablename__ = 'review_reaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)

    reaction_type: Mapped[int] = mapped_column(Enum(ReactionType), index=True)
    review_id: Mapped[int] = mapped_column(ForeignKey(Comment.id), nullable=True)

    review = relationship('Review', back_populates='reactions')
    owner = relationship('User', back_populates='review_reactions')


class CommentReaction(Base):
    __tablename__ = 'comment_reaction'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), nullable=False)

    reaction_type: Mapped[int] = mapped_column(Enum(ReactionType), index=True)
    comment_id: Mapped[int] = mapped_column(ForeignKey(Comment.id), nullable=True)

    comment = relationship('Comment', back_populates='reactions')
    owner = relationship('User', back_populates='comment_reactions')
