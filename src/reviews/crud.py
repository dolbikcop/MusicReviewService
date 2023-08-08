from typing import Any, Type, List, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .enums import ReactionType
from .models import Review, Comment, ReviewReaction
from ..database import DatabaseException


async def db_add_review(db: AsyncSession, **kwargs: Any) -> Review:
    review = Review(**kwargs)
    db.add(review)
    try:
        await db.commit()
        await db.refresh(review)
        return review
    except SQLAlchemyError:
        raise DatabaseException()


async def db_add_comment(db: AsyncSession, **kwargs: Any) -> Comment:
    comment = Comment(**kwargs)
    try:
        db.add(comment)
        await db.commit()
        await db.refresh(comment)
        return comment
    except SQLAlchemyError:
        raise DatabaseException()


async def db_add_review_reaction(db: AsyncSession, **kwargs: Any) -> ReviewReaction:
    reaction = ReviewReaction(**kwargs)
    try:
        db.add(reaction)
        await db.commit()
        await db.refresh(reaction)
        return reaction
    except SQLAlchemyError:
        raise DatabaseException()


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


async def db_get_review_by_id(db: AsyncSession, review_id: int) -> Review | None:
    try:
        await db.commit()
        return await db.get(Review, {'id': review_id})
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_all_user_reviews(db: AsyncSession, review_id: int) -> Sequence[Row | RowMapping | Any]:
    try:
        await db.commit()
        reviews = await db.execute(select(Review).where(Review.owner_id == review_id))
        return reviews.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_all_comments_of_review(db: AsyncSession, review_id: int):
    try:
        await db.commit()
        comments = await db.execute(select(Comment).where(Comment.review_id == review_id))
        return comments.scalars().all()
    except SQLAlchemyError:
        raise DatabaseException()


async def db_add_reaction_to_review(db: AsyncSession, review_id: int, reaction_type: ReactionType):
    pass
