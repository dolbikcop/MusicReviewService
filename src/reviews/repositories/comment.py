from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, NoResultFound

from src.ext import DatabaseException
from src.reviews.models import Comment, CommentReaction
from src.utils.repository import AsyncRepository


class CommentRepository(AsyncRepository):
    async def add(self, **kwargs: Any) -> Comment:
        comment = Comment(**kwargs)
        try:
            self.session.add(comment)
            await self.session.commit()
            await self.session.refresh(comment)
            return comment
        except SQLAlchemyError:
            raise DatabaseException()

    async def get(self, item_id: int) -> Comment | None:
        try:
            await self.session.commit()
            return await self.session.get(Comment, {'id': item_id})
        except SQLAlchemyError:
            raise DatabaseException()

    async def add_reaction(self, **kwargs: Any) -> CommentReaction | None:
        reaction = CommentReaction(**kwargs)
        return self._add_reaction(reaction, reaction.comment_id)

    async def get_reaction(self, item_id: str, owner_id: str) -> CommentReaction | None:
        try:
            reaction = await self.session.execute(select(CommentReaction).where(
                CommentReaction.comment_id == item_id and CommentReaction.owner_id == owner_id))
            return reaction.scalar()
        except NoResultFound:
            return None