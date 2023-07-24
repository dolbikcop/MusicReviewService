from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Review, Comment


async def db_add_review(db: AsyncSession, **kwargs: Any):
    review = Review(**kwargs)
    db.add(review)
    return await db.commit()


async def db_add_comment(db: AsyncSession, **kwargs: Any):
    comment = Comment(**kwargs)
    db.add(comment)
    return await db.commit()


async def db_get_review_by_id(db: AsyncSession, review_id: int):
    await db.commit()
    return await db.get(Review, {'id': review_id})


async def db_get_all_comments_of_review(db: AsyncSession, review_id: int):
    await db.commit()
    comments = await db.execute(select(Comment).where(Comment.review_id == review_id))
    return comments.scalars().all()
