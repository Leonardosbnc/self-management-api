from fastapi import FastAPI

from .routes import main_router


app = FastAPI(
    title="api",
    version="0.1.0",
    description="Organize your life",
)

app.include_router(main_router)
