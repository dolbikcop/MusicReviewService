from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse, JSONResponse, Response

from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyOauthError

from .crud import db_get_user, db_add_user
from .manager import get_current_user
from ..config import CLIENT_SECRET, CLIENT_ID, REDIRECT_URL
from ..database import get_async_session
from ..ext import DatabaseException

router = APIRouter(prefix='/spotify', tags=['spotify', 'auth'])


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="user-library-read")


@router.get('/auth', description="Получения ссылки на авторизацию через Spotify", status_code=200)
async def spotify_get_auth_link(spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth)):
    auth_url = spotify_oauth.get_authorize_url()
    print(auth_url)
    return Response(auth_url, status_code=308)  # status_code=308


@router.get('/callback', description="Авторизация через Spotify при помощи кода авторизации.")
async def spotify_auth(code: str,
                       spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth),
                       db: AsyncSession = Depends(get_async_session)):
    try:
        token = spotify_oauth.get_access_token(code=code, check_cache=False)['access_token']

        print(token)
        user = get_current_user(token)
        db_user = await db_get_user(db, user.id)
        if db_user is None:
            await db_add_user(db, user)

        response = JSONResponse(content=f"Успешная авторизация через Spotify, {user.username}", status_code=201)

        response.set_cookie(key='spotify_token', value=token)
    except SpotifyOauthError:
        response = JSONResponse(content="Неверный код", status_code=400)
    except DatabaseException:
        response = JSONResponse(content='Упс, что-то пошло не так', status_code=500)

    return response
