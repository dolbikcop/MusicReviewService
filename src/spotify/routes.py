from typing import Annotated

from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse

from .auth import get_auth_header
from .service import search
from ..config import BASE_SPOTIFY_TOKEN

router = APIRouter(prefix='/spotify', tags=['spotify'])


@router.get('/search')
async def search_album(spotify_token: Annotated[str | None, Cookie()],
                       query: str, limit: int = 10, offset: int = 0):
    if spotify_token is None:
        spotify_token = BASE_SPOTIFY_TOKEN
    header = get_auth_header(spotify_token)
    try:
        response = search(query, limit, offset, header)
        return response.json()
    except Exception:
        return JSONResponse(content='Не удалось выполнить запрос', status_code=500)
