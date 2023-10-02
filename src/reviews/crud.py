from typing import Any, List, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext import DatabaseException
from .models import Review, Comment


async def db_get_album_reviews(db: AsyncSession, album_id: int | str,
                               limit: int, offset: int) -> List[Review] | None:
    try:
        await db.commit()
        reviews = await db.execute(select(Review)
                                   .where(Review.album_id == album_id)
                                   .limit(limit)
                                   .offset(offset))
        return reviews.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_all_user_reviews(db: AsyncSession, owner_id: int) -> Sequence[Row | RowMapping | Any]:
    try:
        await db.commit()
        reviews = await db.execute(select(Review).where(Review.owner_id == owner_id))
        return reviews.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_all_comments_of_review(db: AsyncSession, review_id: int) -> Sequence[Row | RowMapping | Any]:
    try:
        await db.commit()
        comments = await db.execute(select(Comment).where(Comment.review_id == review_id))
        return comments.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_most_popular_reviews(db: AsyncSession,
                                      limit, offset: int) -> Sequence[Row | RowMapping | Any]:
    try:
        reviews = await db.execute(select(Review)
                                   .order_by(Review.likes + Review.dislikes)
                                   .limit(limit)
                                   .offset(offset))
        return reviews.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()
