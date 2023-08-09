from typing import Dict, Any

import requests

from src.ext import APIException, UnauthorizedException

BASE_URL = 'https://api.spotify.com/v1/'


def search(query: str, limit: int, offset: int, headers: Dict[str, Any]):
    url = BASE_URL + 'search'
    params = {
        'q': query,
        'type': 'album',
        'limit': limit,
        'offset': offset
    }
    response = requests.get(url, params=params, headers=headers).json()
    print(response)
    if response.get('error') is not None:
        raise UnauthorizedException if response['error']['status'] == 401 else APIException
    result = []
    for i in response['albums']['items']:
        result.append({
            'name': i['name'],
            'id': i['id'],
            'artists': [a['name'] for a in i['artists']],
            'album_type': i['album_type'],
            'release_date': i['release_date'],
            'image': i['images'][0]['url'],
            'url': i['external_urls']['spotify']
        })
    return result


def get_album_info(id: str, headers: Dict[str, Any]) -> Dict[str, Any] | None:
    url = BASE_URL + 'albums/' + id
    response = requests.get(url, headers=headers).json()
    print(response)
    if response.get('error') is not None:
        raise UnauthorizedException if response['error']['status'] == 401 else APIException
    info = {
        'name': response['name'],
        'artists': [artist['name'] for artist in response['artists']],
        'release_date': response['release_date'],
        'genres': response['genres'],
        'label': response['label']
    }
    return info

