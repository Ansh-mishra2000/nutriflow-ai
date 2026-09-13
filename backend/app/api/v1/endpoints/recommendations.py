from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.health import HealthAssessmentRequest
from app.schemas.meal import DayPlanResponse
from app.services.nutrition_engine import NutritionEngine
from app.services.recommender import RecommenderService

router = APIRouter()

@router.post("/day-plan", response_model=DayPlanResponse, summary="Generate Complete Daily Meal & Workout Plan")
def generate_day_plan(
    request: HealthAssessmentRequest,
    db: Session = Depends(get_db)
):
    """
    Calculates health assessment and matches curated nutritious meals and custom
    workout routines to the user's physiological profile and dietary preferences.
    """
    health_eval = NutritionEngine.evaluate_health(request)
    day_plan = RecommenderService.generate_day_plan(
        db=db,
        health=health_eval,
        goal=request.goal,
        diet_preference=request.diet_preference,
        variation=request.variation or 0
    )
    return day_plan
