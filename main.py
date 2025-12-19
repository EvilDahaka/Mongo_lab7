import pathlib
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from app.auth.user_manager import auth_backend, fastapi_users
from app.database.connection import close_db, init_db
from app.routers import categories, posts, stats
from app.schemas.user import UserCreate, UserRead


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(title="Blog System API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows specific origins
    allow_credentials=True,  # Allows cookies to be sent cross-origin
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Auth routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix="/users",
    tags=["users"],
)

# API routes
app.include_router(posts.router, prefix="/api", tags=["posts"])
app.include_router(categories.router, prefix="/api", tags=["categories"])
app.include_router(stats.router, prefix="/api", tags=["stats"])


@app.get("/", response_class=HTMLResponse)
async def read_root():
    html_path = pathlib.Path("templates/index.html")
    return HTMLResponse(content=html_path.read_text(), status_code=200)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
