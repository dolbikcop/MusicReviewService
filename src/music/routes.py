from typing import Union

from fastapi import APIRouter

from .schemas import SearchResponse

router = APIRouter(prefix='/music', tags=['music'])


@router.get('/search', response_model=SearchResponse)
async def search_music(text: str):
    return


@router.get('/track')
async def get_track_by_id(id: Union[int, str]):
    return
