from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from .crud import db_add_review, db_add_comment, db_get_review_by_id, db_get_all_comments_of_review
from .schemas import ReviewCreate, CommentCreate
from ..auth.config import current_user
from ..auth.models import User
from ..database import get_async_session

router = APIRouter(tags=['review'])


@router.post('/{album_id}/reviews')
async def add_review(album_id: Union[int, str],
                     review_scheme: ReviewCreate,
                     user: User = Depends(current_user),
                     db: AsyncSession = Depends(get_async_session)):
    review = review_scheme.model_dump()
    review['album_id'] = album_id
    review['owner_id'] = user.id
    return await db_add_review(db, **review)


@router.post('/{review_id}/comments')
async def add_comment(review_id: int,
                      comment_scheme: CommentCreate,
                      user: User = Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    review = await db_get_review_by_id(db, review_id)
    if not review:
        return JSONResponse(status_code=404, content="Can't found review")
    comment = comment_scheme.model_dump()
    comment['review_id'] = review.id
    comment['owner_id'] = user.id
    return await db_add_comment(db, **comment)


@router.get('/{review_id}/comments')
async def get_all_comments(review_id: int,
                           db: AsyncSession = Depends(get_async_session)):
    # review = await db_get_review_by_id(db, review_id)
    # if not review:
    #     return JSONResponse(status_code=404, content="Can't found review")
    return await db_get_all_comments_of_review(db, review_id)
