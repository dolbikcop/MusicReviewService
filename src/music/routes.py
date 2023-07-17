from typing import Union

from fastapi import APIRouter
from . import schemas

router = APIRouter(prefix='/music', tags=['music'])


@router.get('/search', response_model=schemas.SearchResponse)
def search_music(request: schemas.SearchRequest):
    pass


@router.get('/track')
def get_track_by_id(id: Union[int, str]):
    pass
