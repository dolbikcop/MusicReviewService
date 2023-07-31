from fastapi import APIRouter, Depends
from starlette.responses import RedirectResponse, JSONResponse

from spotipy import SpotifyOAuth
from spotipy.oauth2 import SpotifyOauthError

from ..config import CLIENT_SECRET, CLIENT_ID, REDIRECT_URL

router = APIRouter(prefix='/spotify', tags=['spotify'])


def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URL,
        scope="user-library-read")


@router.get('/auth/link', description="Получения ссылки на авторизацию через Spotify")
async def spotify_get_auth_link(spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth)):
    auth_url = spotify_oauth.get_authorize_url()
    print(auth_url)
    return RedirectResponse(auth_url, status_code=200)


@router.get('/auth', description="Авторизация через Spotify при помощи кода авторизации.")
async def spotify_auth(code: str,
                       spotify_oauth: SpotifyOAuth = Depends(create_spotify_oauth)):
    try:
        token = spotify_oauth.get_access_token(code=code, check_cache=False)['access_token']

        response = JSONResponse(content="Successful spotify authorization", status_code=200)
        response.set_cookie(key='spotify_token', value=token)
    except SpotifyOauthError:
        content = "Invalid code"
        response = JSONResponse(content=content, status_code=400)

    return response




