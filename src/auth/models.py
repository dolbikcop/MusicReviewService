from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(String, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(length=100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship('Review', backref='owner', cascade='all, delete-orphan')
    comments = relationship('Comment', backref='owner', cascade='all, delete-orphan')

    review_reactions = relationship('ReviewReaction', backref='owner', cascade='all, delete-orphan')
    comment_reactions = relationship('CommentReaction', backref='owner', cascade='all, delete-orphan')

