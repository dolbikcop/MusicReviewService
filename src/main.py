from fastapi import FastAPI

from .spotify.auth import auth_router as music_router
from .spotify.routes import router as spotify_router
from .auth.config import router as auth_router
from .reviews.routes import router as review_router

app = FastAPI()

app.include_router(music_router)
app.include_router(auth_router)
app.include_router(review_router)
app.include_router(spotify_router)

