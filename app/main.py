from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routes import router
from .settings import get_settings


settings = get_settings()

app = FastAPI(
    title="ComicCraft AI",
    description="AI-powered comic generator",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory=settings.static_dir),
    name="static",
)

app.include_router(router)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "message": "ComicCraft AI is running",
    }