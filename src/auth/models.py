from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(length=100), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    reviews = relationship('Review', back_populates='owner', cascade='all, delete-orphan')
    comments = relationship('Comment', back_populates='owner', cascade='all, delete-orphan')

    review_reactions = relationship('ReviewReaction', back_populates='owner', cascade='all, delete-orphan')
    comment_reactions = relationship('CommentReaction', back_populates='owner', cascade='all, delete-orphan')
