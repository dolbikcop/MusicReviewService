import json
from typing import Union

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, Response

from .crud import db_add_review, db_add_comment, db_get_review_by_id, db_get_all_comments_of_review, DatabaseException
from .schemas import ReviewCreate, CommentCreate, CommentRead
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
    try:
        review = await db_add_review(db, **review)
        return JSONResponse(f'Добавлено ревью: id - {review.id}', status_code=200)
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить рецензию', status_code=500)


@router.post('/{review_id}/comments')
async def add_comment(review_id: int,
                      comment_scheme: CommentCreate,
                      user: User = Depends(current_user),
                      db: AsyncSession = Depends(get_async_session)):
    review = await db_get_review_by_id(db, review_id)
    if not review:
        return JSONResponse(status_code=404, content="Ревью не найдено")
    comment = comment_scheme.model_dump()
    comment['review_id'] = review.id
    comment['owner_id'] = user.id
    try:
        comment = await db_add_comment(db, **comment)
        return JSONResponse(status_code=200,
                            content=f"Добавлен комментарий для ревью {comment.review_id}: comment_id - {comment.id}")
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить комментарий', status_code=500)


@router.get('/{review_id}/comments', status_code=200)
async def get_all_comments(review_id: int,
                           db: AsyncSession = Depends(get_async_session)):
    review = await db_get_review_by_id(db, review_id)
    if not review:
        return JSONResponse(status_code=404, content="Ревью не найдено")
    try:
        comments = await db_get_all_comments_of_review(db, review_id)
        comments_read = [CommentRead(id=comment.id,
                                     owner_id=comment.owner_id,
                                     text=comment.text,
                                     likes=comment.likes,
                                     dislikes=comment.dislikes)
                         for comment in comments]
        return comments_read
    except DatabaseException:
        return JSONResponse('Упс, не удалось найти комментарии', status_code=500)
