from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import settings
from app.database import init_db, close_db
from app.api import tasks, users

# Lifespan context manager for startup/shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI app
app = FastAPI(
    title="FastAPI Celery MongoDB Demo",
    description="A FastAPI application with Celery background workers and MongoDB using Beanie",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "FastAPI Celery MongoDB Demo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


@app.get("/info")
async def api_info():
    """API information and available endpoints"""
    return {
        "name": "FastAPI Celery MongoDB Demo",
        "description": "A comprehensive FastAPI application with background task processing",
        "features": [
            "FastAPI with async/await support",
            "Celery background workers",
            "MongoDB with Beanie ODM",
            "Redis as message broker",
            "Task management with status tracking",
            "User management",
            "Task execution logs",
            "Statistics and reporting"
        ],
        "endpoints": {
            "tasks": "/tasks",
            "users": "/users",
            "docs": "/docs",
            "health": "/health"
        }
    } 