from fastapi import FastAPI

from .auth.routes import router as auth_router
from .spotify.routes import router as spotify_router
from .reviews.routes import router as review_router

app = FastAPI(title='MusView')

app.include_router(auth_router)
app.include_router(review_router)
app.include_router(spotify_router)

