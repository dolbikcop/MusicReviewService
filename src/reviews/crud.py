from typing import Any, List, Sequence

from sqlalchemy import select, Row, RowMapping
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext import DatabaseException
from .enums import ReactionType
from .models import Review, Comment, ReviewReaction, CommentReaction


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


async def db_add_review_reaction(db: AsyncSession, **kwargs: Any) -> ReviewReaction | None:
    reaction = ReviewReaction(**kwargs)
    try:
        review = await db_get_review_by_id(db, reaction.review_id)
        same_react = await db_get_review_reaction(db, reaction.review_id, reaction.owner_id)
        if same_react is not None:
            await db.delete(same_react)
            if same_react.reaction_type == ReactionType.like:
                review.likes -= 1
            else:
                review.dislikes -= 1
            if same_react.reaction_type == reaction.reaction_type:
                await db.commit()
                return None
        if reaction.reaction_type == ReactionType.like:
            review.likes += 1
        else:
            review.dislikes += 1
        db.add(reaction)
        await db.commit()
        await db.refresh(reaction)
        return reaction
    except SQLAlchemyError:
        raise DatabaseException()


async def db_add_comment_reaction(db: AsyncSession, **kwargs: Any) -> CommentReaction | None:
    reaction = CommentReaction(**kwargs)
    try:
        comment = await db_get_comment_by_id(db, reaction.comment_id)
        same_react = await db_get_comment_reaction(db, reaction.comment_id, reaction.owner_id)
        if same_react is not None:
            await db.delete(same_react)
            if same_react.reaction_type == ReactionType.like:
                comment.likes -= 1
            else:
                comment.dislikes -= 1
            if same_react.reaction_type == reaction.reaction_type:
                await db.commit()
                return None
        if reaction.reaction_type == ReactionType.like:
            comment.likes += 1
        else:
            comment.dislikes += 1
        db.add(reaction)
        await db.commit()
        await db.refresh(reaction)
        return reaction
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_review_reaction(db: AsyncSession, review_id: str, owner_id: str) -> ReviewReaction | None:
    try:
        reaction = await db.execute(select(ReviewReaction).where(
            ReviewReaction.review_id == review_id and ReviewReaction.owner_id == owner_id))
        return reaction.scalar()
    except NoResultFound:
        return None


async def db_get_comment_reaction(db: AsyncSession, comment_id: str, owner_id: str) -> CommentReaction | None:
    try:
        reaction = await db.execute(select(CommentReaction).where(
            CommentReaction.comment_id == comment_id and CommentReaction.owner_id == owner_id))
        return reaction.scalar()
    except NoResultFound:
        return None


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


async def db_get_comment_by_id(db: AsyncSession, comment_id: int) -> Comment | None:
    try:
        await db.commit()
        return await db.get(Comment, {'id': comment_id})
    except SQLAlchemyError:
        raise DatabaseException()


async def db_get_all_user_reviews(db: AsyncSession, review_id: int) -> Sequence[Row | RowMapping | Any]:
    try:
        await db.commit()
        reviews = await db.execute(select(Review).where(Review.owner_id == review_id))
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
