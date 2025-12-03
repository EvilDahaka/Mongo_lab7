from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

# Authentication
from app.auth.user_manager import auth_backend, fastapi_users
from app.database.connection import init_db
from app.routers import categories, posts, stats
from app.schemas.user import UserCreate, UserRead, UserUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events"""
    # Startup - initialize Beanie
    await init_db()
    yield
    # Shutdown - nothing special required


# Create FastAPI app
app = FastAPI(
    title="Blog System API",
    description="REST API for a blog system using Beanie ODM",
    version="1.0.0",
    lifespan=lifespan,
)

# Include routers
app.include_router(posts)
app.include_router(categories)
app.include_router(stats)

# Auth routers (FastAPI Users)
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# Static files
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = Path("templates/index.html")
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return HTMLResponse("<h1>Blog System</h1>")


@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Blog API is running"}
