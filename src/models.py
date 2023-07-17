from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, func
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    registered_at = Column(DateTime(timezone=True), server_default=func.now())

    reviews = relationship('Review', back_populates='owner')
    comments = relationship('Comment', back_populates='owner')


class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    review_id = Column(Integer, ForeignKey('reviews.review_id'))

    owner = relationship("User", back_populates="comments")


class Review(Base):
    __tablename__ = "reviews"

    review_id = Column(Integer, primary_key=True, index=True)
    grade = Column(Float, index=True)
    text = Column(String)
    owner_id = Column(Integer, ForeignKey("users.user_id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    #TODO: create track, artist, album binding
    #TODO: create comment binding

    owner = relationship("User", back_populates="reviews")
