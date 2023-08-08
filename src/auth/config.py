import redis as redis
from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, CookieTransport, RedisStrategy

from .manager import get_user_manager
from .models import User
from .routes import router as register_router
from ..config import REDIS_URL

cookie_transport = CookieTransport(cookie_max_age=3600)
redis = redis.asyncio.from_url(REDIS_URL, decode_responses=True)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis, lifetime_seconds=3600)




auth_backend = AuthenticationBackend(
    name="auth",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router = APIRouter(prefix="/auth", tags=["auth"])
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(register_router)


