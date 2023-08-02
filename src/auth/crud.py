from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.database import DatabaseException, get_async_session


async def db_get_user_with_name(name: str, db: AsyncSession) -> User | None:
    try:
        user = await db.execute(select(User).where(User.username == name))
        return user.scalar()
    except SQLAlchemyError:
        raise DatabaseException()


