# Blog System (Beanie + FastAPI + MongoDB)

A complete FastAPI blog application using Beanie (ODM for MongoDB) with authentication, pagination, and a Bootstrap UI.

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

**Full stack (FastAPI + MongoDB):**

```bash
docker-compose up -d
```

The app will be available at `http://localhost:8000`
MongoDB at `localhost:27017`
API docs at `http://localhost:8000/docs`

**For development (MongoDB only, run FastAPI locally):**

```bash
docker-compose -f docker-compose-dev.yml up -d
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Local Development

1. **Create and activate virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. **Start MongoDB:**

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
```

3. **Copy `.env.example` to `.env`:**

```bash
cp .env.example .env
```

4. **Run the app:**

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📚 API Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔐 Authentication

- **Register:** `POST /auth/register`
- **Login:** `POST /auth/jwt/login`
- **Users:** `GET /users` (get current user with token)

## 📝 Available Endpoints

### Posts
- `GET /api/posts` - List all published posts (paginated)
- `GET /api/posts/{post_id}` - Get single post
- `POST /api/posts` - Create post (requires auth)
- `GET /api/posts/search/?q=query` - Search posts (paginated)
- `GET /api/posts/category/{category_id}` - Posts by category
- `GET /api/posts/tag/{tag}` - Posts by tag

### Categories
- `GET /api/categories` - List all categories
- `GET /api/categories/{category_id}` - Get single category

### Statistics
- `GET /api/stats/top-authors` - Top authors by posts
- `GET /api/stats/popular-categories` - Popular categories
- `GET /api/stats/comments-stats` - Comments statistics
- `GET /api/stats/tags-distribution` - Tag distribution

## 🛑 Stop & Clean Up

```bash
# Stop containers
docker-compose down

# Remove all data (including MongoDB volumes)
docker-compose down -v

# Stop development MongoDB only
docker-compose -f docker-compose-dev.yml down
```

## 📋 Project Structure

```
blog_system/
├── main.py                    # FastAPI entrypoint
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker build config
├── docker-compose.yml         # Production compose file
├── docker-compose-dev.yml     # Dev compose file (MongoDB only)
├── .env.example              # Env template
├── README.md                 # This file
│
├── app/
│   ├── config.py            # Settings
│   ├── models/              # Beanie ODM models
│   │   ├── user.py
│   │   ├── post.py
│   │   └── category.py
│   ├── schemas/             # Pydantic API schemas
│   │   ├── user.py
│   │   ├── post.py
│   │   ├── pagination.py
│   ├── services/            # Business logic
│   │   └── post_service.py
│   ├── routers/             # API endpoints
│   │   ├── posts.py
│   │   ├── categories.py
│   │   └── stats.py
│   ├── auth/                # Authentication
│   │   └── user_manager.py
│   └── database/            # DB connection
│       └── connection.py
│
├── templates/
│   └── index.html           # Bootstrap UI
└── static/                  # Static files
```

## 🔧 Environment Variables

Copy `.env.example` to `.env`:

```env
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=blog_system
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=true
SECRET_KEY=change-me-in-production
```

For Docker Compose with auth:
```env
MONGODB_URL=mongodb://root:example@mongodb:27017
```

## 💾 Database

MongoDB collections:
- `users` - User accounts with profiles
- `posts` - Blog posts with embedded author/category
- `categories` - Blog categories

## 🎨 Frontend

Bootstrap 5 based UI at `http://localhost:8000` with:
- Posts listing with pagination
- Search functionality
- User registration/login
- Create post form (for authenticated users)

---

**Built with:** FastAPI • Beanie • MongoDB • Pydantic • Bootstrap 5
