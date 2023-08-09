from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from ..ext import DatabaseException


async def db_get_user(db: AsyncSession, id: str) -> User | None:
    try:
        return await db.get(User, {'id': id})
    except SQLAlchemyError:
        raise DatabaseException


async def db_add_user(db: AsyncSession, user: User) -> User | None:
    try:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    except SQLAlchemyError:
        raise DatabaseException
