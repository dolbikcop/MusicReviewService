from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.ext import DatabaseException
from src.reviews.models import Review, ReviewReaction
from src.utils.repository import AsyncRepository


class ReviewRepository(AsyncRepository):
    async def add(self, **kwargs: Any) -> Review:
        review = Review(**kwargs)
        self.session.add(review)
        try:
            await self.session.commit()
            await self.session.refresh(review)
            return review
        except SQLAlchemyError:
            raise DatabaseException()

    async def get(self, item_id: int) -> Review | None:
        try:
            await self.session.commit()
            return await self.session.get(Review, {'id': item_id})
        except SQLAlchemyError:
            raise DatabaseException()

    async def add_reaction(self, **kwargs: Any) -> ReviewReaction | None:
        reaction = ReviewReaction(**kwargs)
        return self._add_reaction(reaction, reaction.review_id)

    async def get_reaction(self, item_id: str, owner_id: str) -> ReviewReaction | None:
        try:
            reaction = await self.session.execute(select(ReviewReaction).where(
                ReviewReaction.review_id == item_id and ReviewReaction.owner_id == owner_id))
            return reaction.scalar()
        except NoResultFound:
            return None