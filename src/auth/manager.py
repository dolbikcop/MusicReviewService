import requests

from src.ext import UnauthorizedException
from .models import User


def get_current_user(token: str) -> User:
    url = 'https://api.spotify.com/v1/me'
    header = get_auth_header(token)

    response = requests.get(url, headers=header)
    print(response.json())
    if response.status_code == 401:
        raise UnauthorizedException
    json = response.json()
    return User(id=json['id'], username=json['display_name'])


def get_auth_header(token: str):
    if token is None:
        raise UnauthorizedException
    return {'Authorization': f'Bearer {token}'}
