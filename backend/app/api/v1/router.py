from fastapi import APIRouter
from app.api.v1.endpoints import health, recommendations, catalog, orders, ai_coach, auth

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["Clinical Health Assessment"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["AI Meal & Workout Plans"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["Food & Meal Catalog"])
api_router.include_router(orders.router, prefix="/orders", tags=["Food Ordering & Delivery Tracking"])
api_router.include_router(ai_coach.router, prefix="/ai-coach", tags=["AI Nutritionist Coach"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication & Profiles"])
