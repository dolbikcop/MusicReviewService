from abc import ABC
from typing import Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.ext import DatabaseException
from src.reviews.enums import ReactionType


class AsyncRepository(ABC):
    def __init__(self, db: AsyncSession):
        self.session = db

    async def add(self, **kwargs: Any):
        pass

    async def get(self, item_id: int | str):
        pass

    async def add_reaction(self, **kwargs: Any):
        pass

    async def get_reaction(self, item_id: str, owner_id: str):
        pass

    async def _add_reaction(self, reaction, item_id):
        try:
            review = await self.get(item_id)
            same_react = await self.get_reaction(item_id, reaction.owner_id)
            if same_react:
                await self.session.delete(same_react)
                if same_react.reaction_type == ReactionType.like:
                    review.likes -= 1
                else:
                    review.dislikes -= 1
                if same_react.reaction_type == reaction.reaction_type:
                    await self.session.commit()
                    return None
            if reaction.reaction_type == ReactionType.like:
                review.likes += 1
            else:
                review.dislikes += 1
            self.session.add(reaction)
            await self.session.commit()
            await self.session.refresh(reaction)
            return reaction
        except SQLAlchemyError:
            raise DatabaseException()