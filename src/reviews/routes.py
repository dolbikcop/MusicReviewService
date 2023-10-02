from typing import Union

from fastapi import APIRouter, Depends, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from .crud import db_get_all_comments_of_review, db_get_album_reviews, db_get_most_popular_reviews
from .enums import ReactionType
from .repositories.comment import CommentRepository
from .repositories.review import ReviewRepository
from .schemas import ReviewCreate, CommentCreate, CommentRead, ReviewRead
from ..auth.manager import get_auth_header, get_current_user
from ..database import get_async_session
from ..ext import UnauthorizedException, APIException, DatabaseException
from ..spotify.service import get_album_info

router = APIRouter()

session = get_async_session()
comment_rep = CommentRepository(session)
review_rep = ReviewRepository(session)


@router.post('/{album_id}/reviews', tags=['album', 'review'])
async def add_review(album_id: Union[int, str],
                     review_scheme: ReviewCreate,
                     spotify_token: Union[str | None] = Cookie(default=None)):
    try:
        header = get_auth_header(spotify_token)
        if get_album_info(album_id, header):
            review = review_scheme.model_dump()
            review['album_id'] = album_id
            review['owner_id'] = get_current_user(spotify_token).id
            review = await review_rep.add(**review)
            return JSONResponse(f'Добавлено ревью: id - {review.id}', status_code=200)
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить рецензию', status_code=500)
    except UnauthorizedException:
        return JSONResponse(status_code=401, content='Пожалуйста, авторизуйтесь через Spotify')
    except APIException:
        return JSONResponse('Упс, не удалось найти альбом', status_code=404)


@router.get('/{album_id}/reviews', tags=['album', 'review'])
async def get_album_reviews(album_id: str,
                            limit: int = 10,
                            offset: int = 0,
                            db: AsyncSession = Depends(get_async_session)):
    try:
        reviews = await db_get_album_reviews(db, album_id, limit, offset)
        print(reviews[0].id)
        reviews_read = [ReviewRead(id=review.id,
                                   owner_id=review.owner_id,
                                   text=review.text,
                                   grade=review.grade,
                                   pros=review.pros,
                                   cons=review.cons,
                                   likes=review.likes,
                                   dislikes=review.dislikes,
                                   created_at=review.created_at)
                        for review in reviews]
        return reviews_read
    except DatabaseException:
        return JSONResponse('Упс, не удалось найти ревью', status_code=500)


@router.post('/{review_id}/comments', tags=['comment', 'review'])
async def add_comment(review_id: int,
                      comment_scheme: CommentCreate,
                      spotify_token: Union[str | None] = Cookie(default=None)):
    review = await review_rep.get(review_id)
    if not review:
        return JSONResponse(status_code=404, content="Ревью не найдено")
    try:
        comment = comment_scheme.model_dump()
        comment['review_id'] = review.id
        comment['owner_id'] = get_current_user(spotify_token).id
        comment = await comment_rep.add(**comment)
        return JSONResponse(status_code=200,
                            content=f"Добавлен комментарий для ревью {comment.review_id}: comment_id - {comment.id}")
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить комментарий', status_code=500)
    except UnauthorizedException:
        return JSONResponse(status_code=401, content='Пожалуйста, авторизуйтесь через Spotify')


@router.post('/reviews/{review_id}/reaction', tags=['reaction', 'review'])
async def add_or_remove_reaction_to_review(review_id: int,
                                           reaction_type: ReactionType,
                                           spotify_token: Union[str | None] = Cookie(default=None)):
    review = await review_rep.get(review_id)
    if not review:
        return JSONResponse(status_code=404, content="Ревью не найдено")
    try:
        reaction = {'reaction_type': reaction_type,
                    'review_id': review.id,
                    'owner_id': get_current_user(spotify_token).id}
        reaction = await review_rep.add_reaction(**reaction)
        if reaction is not None:
            return JSONResponse(status_code=201,
                                content=f"Добавлена реакция для ревью {reaction.review_id}: "
                                        f"reaction_type - {reaction.reaction_type}")
        else:
            return JSONResponse(status_code=200,
                                content=f"Удалена реакция для ревью {review_id}: "
                                        f"reaction_type - {reaction_type}")
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить комментарий', status_code=500)
    except UnauthorizedException:
        return JSONResponse(status_code=401, content='Пожалуйста, авторизуйтесь через Spotify')


@router.post('/comments/{comment_id}/reaction', tags=['comment', 'reaction'])
async def add_or_remove_reaction_to_comment(comment_id: int,
                                            reaction_type: ReactionType,
                                            spotify_token: Union[str | None] = Cookie(default=None)):
    comment = await comment_rep.get(comment_id)
    if not comment:
        return JSONResponse(status_code=404, content="Комментарий не найден")
    try:
        reaction = {'reaction_type': reaction_type,
                    'comment_id': comment.id,
                    'owner_id': get_current_user(spotify_token).id}
        reaction = await comment_rep.get_reaction(**reaction)
        if reaction is not None:
            return JSONResponse(status_code=201,
                                content=f"Добавлена реакция для комментария {reaction.comment_id}: "
                                        f"reaction_type - {reaction.reaction_type}")
        else:
            return JSONResponse(status_code=200,
                                content=f"Удалена реакция для комментария {comment_id}: "
                                        f"reaction_type - {reaction_type}")
    except DatabaseException:
        return JSONResponse('Упс, не удалось добавить комментарий', status_code=500)
    except UnauthorizedException:
        return JSONResponse(status_code=401, content='Пожалуйста, авторизуйтесь через Spotify')


@router.get('/{review_id}/comments', status_code=200, tags=['comment', 'review'])
async def get_all_comments(review_id: int,
                           db: AsyncSession = Depends(get_async_session)):
    review = await review_rep.get(review_id)
    if not review:
        return JSONResponse(status_code=404, content="Ревью не найдено")
    try:
        comments = await db_get_all_comments_of_review(db, review_id)
        comments_read = [CommentRead(id=comment.id,
                                     owner_id=comment.owner_id,
                                     text=comment.text,
                                     likes=comment.likes,
                                     dislikes=comment.dislikes,
                                     created_at=comment.created_at)
                         for comment in comments]
        return comments_read
    except DatabaseException:
        return JSONResponse('Упс, не удалось найти комментарии', status_code=500)


@router.get('/', tags=['review'])
async def get_most_reacted_reviews(limit: int = 10,
                                   offset: int = 0,
                                   db: AsyncSession = Depends(get_async_session)):
    try:
        reviews = await db_get_most_popular_reviews(db, limit, offset)
        reviews_read = [ReviewRead(id=review.id,
                                   owner_id=review.owner_id,
                                   text=review.text,
                                   grade=review.grade,
                                   pros=review.pros,
                                   cons=review.cons,
                                   likes=review.likes,
                                   dislikes=review.dislikes,
                                   created_at=review.created_at)
                        for review in reviews]
        return reviews_read
    except DatabaseException:
        return JSONResponse('Упс, что-то пошло не так', status_code=500)
