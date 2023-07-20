import uvicorn
from fastapi import FastAPI

from .music.routes import router as music_router
from .auth.config import router as auth_router

app = FastAPI()

app.include_router(music_router)
app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)

