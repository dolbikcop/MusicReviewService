from typing import Optional

from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin, schemas, models, exceptions
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from .crud import db_get_user_with_name
from .models import User
from ..config import RESET_TOKEN, VERIFICATION_TOKEN
from ..database import get_async_session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = RESET_TOKEN
    verification_token_secret = VERIFICATION_TOKEN



async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
