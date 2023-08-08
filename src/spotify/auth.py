from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse, JSONResponse

from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyOauthError

from ..auth.config import current_user
from ..auth.models import User
from ..config import CLIENT_SECRET, CLIENT_ID, REDIRECT_URL

auth_router = APIRouter(prefix='/spotify/auth', tags=['spotify', 'auth'])


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="user-library-read")


@auth_router.get('/link', description="Получения ссылки на авторизацию через Spotify")
async def spotify_get_auth_link(spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth),
                                user: User = Depends(current_user)):
    auth_url = spotify_oauth.get_authorize_url()
    print(auth_url)
    return RedirectResponse(auth_url, status_code=200)


@auth_router.get('', description="Авторизация через Spotify при помощи кода авторизации.")
async def spotify_auth(code: str,
                       spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth),
                       user: User = Depends(current_user)):
    try:
        token = spotify_oauth.get_access_token(code=code, check_cache=False)['access_token']

        response = JSONResponse(content="Successful spotify authorization", status_code=200)
        response.set_cookie(key='spotify_token', value=token)
    except SpotifyOauthError:
        content = "Invalid code"
        response = JSONResponse(content=content, status_code=400)

    return response


def get_auth_header(token: str):
    return {'Authorization': f'Bearer {token}'}
