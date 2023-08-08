from typing import Dict, Any

import requests

BASE_URL = 'https://api.spotify.com/v1/'


def search(query: str, limit: int, offset: int, headers: Dict[str, Any]):
    url = BASE_URL + 'search'
    params = {
        'q': query,
        'type': 'album',
        'limit': limit,
        'offset': offset
    }
    response = requests.get(url, params=params, headers=headers)
    return response


def get_album_info(id: str, headers: Dict[str, Any]) -> Dict[str, Any] | None:
    url = BASE_URL + 'albums/' + id
    response = requests.get(url, headers).json()
    if response is None:
        return None
    info = {
        'name': response['name'],
        'artists': [artist['name'] for artist in response['artists']],
        'release_date': response['release_date'],
        'genres': response['genres'],
        'label': response['label']
    }
    return info

