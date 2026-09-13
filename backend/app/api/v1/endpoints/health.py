from fastapi import APIRouter
from app.schemas.health import HealthAssessmentRequest, HealthAssessmentResponse
from app.services.nutrition_engine import NutritionEngine

router = APIRouter()

@router.post("/calculate", response_model=HealthAssessmentResponse, summary="Calculate BMI, BMR, TDEE & Target Macros")
def calculate_health_metrics(request: HealthAssessmentRequest):
    """
    Computes clinical health metrics:
    - **BMI** and health categorization
    - **BMR** using the gold-standard Mifflin-St Jeor equation
    - **TDEE** based on verified activity level multipliers
    - **Target Calorie & Macronutrient targets** tailored to weight loss, maintenance, or muscle gain
    - **Meal-by-meal calorie distributions** (Breakfast, Lunch, Dinner, Snacks)
    - Optional **US Navy Body Fat %** if tape measurements are provided
    """
    return NutritionEngine.evaluate_health(request)
