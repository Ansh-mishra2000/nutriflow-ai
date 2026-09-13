import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1.router import api_router
from app.db.init_db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="""
# 🥗 NutriFlow AI API
### Cloud-Native Health, AI Nutrition Planning & Calorie-Optimized Food Delivery Platform

- **Health Assessment**: Clinical BMI, Mifflin-St Jeor BMR, TDEE, Body Fat estimation, and custom macro targets.
- **AI Recommendation**: Automatic meal-by-meal budget allocation for Breakfast, Lunch, Dinner, and Snacks.
- **Food Delivery Module**: Food catalog with detailed nutrient sheets, cart checkout, and real-time delivery state tracker.
- **AI Nutrition Coach**: Intelligent recipe customization and nutritional Q&A powered by Google Gemini API.
    """,
    version="2.0.0",
    lifespan=lifespan
)

# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

# Serve Frontend SPA
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/", tags=["UI & Dashboard"])
def read_root():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "2.0.0",
        "docs": "/docs"
    }
