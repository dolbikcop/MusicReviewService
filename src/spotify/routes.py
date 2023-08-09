from typing import Union

from fastapi import APIRouter, Cookie
from starlette.responses import JSONResponse

from .service import search
from ..auth.manager import get_auth_header
from ..ext import APIException, UnauthorizedException

router = APIRouter(tags=['spotify', 'album'])


@router.get('/search')
async def search_album(query: str, limit: int = 10, offset: int = 0,
                       spotify_token: Union[str | None] = Cookie(default=None)):
    try:
        header = get_auth_header(spotify_token)
        response = search(query, limit, offset, header)
        return response
    except APIException:
        return JSONResponse(content='Не удалось выполнить запрос', status_code=500)
    except UnauthorizedException:
        return JSONResponse(content='Авторизуйтесь через Spotify', status_code=401)
