from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class FoodItemBase(BaseModel):
    name: str
    category: str
    description: Optional[str] = None
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    price: float
    diet_type: str = "any"
    image_url: Optional[str] = None
    prep_time_mins: int = 15
    ingredients: Optional[str] = None

class FoodItemCreate(FoodItemBase):
    pass

class FoodItemResponse(FoodItemBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class MealRecommendation(BaseModel):
    category: str
    target_calories: float
    recommended_food: FoodItemResponse
    calorie_variance: float
    alternative_foods: List[FoodItemResponse] = []

class WorkoutRecommendation(BaseModel):
    title: str
    type: str
    intensity: str
    duration_mins: int
    exercises: List[str]
    description: str

class DayPlanResponse(BaseModel):
    health_summary: dict
    total_plan_calories: float
    total_plan_protein: float
    total_plan_carbs: float
    total_plan_fat: float
    meals: List[MealRecommendation]
    workout: WorkoutRecommendation
