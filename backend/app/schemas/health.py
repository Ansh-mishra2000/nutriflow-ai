from pydantic import BaseModel, Field
from typing import Optional, Dict

class HealthAssessmentRequest(BaseModel):
    age: int = Field(..., ge=10, le=120, description="Age in years")
    gender: str = Field(..., pattern="^(male|female|other)$", description="Gender: male, female, or other")
    height_cm: float = Field(..., ge=50, le=260, description="Height in centimeters")
    weight_kg: float = Field(..., ge=20, le=350, description="Weight in kilograms")
    activity_level: str = Field(
        "sedentary",
        pattern="^(sedentary|light|moderate|active|very_active)$",
        description="Physical activity level"
    )
    goal: str = Field(
        "maintenance",
        pattern="^(weight_loss|maintenance|muscle_gain)$",
        description="Health and fitness goal"
    )
    diet_preference: Optional[str] = Field("any", description="Dietary preference: any, vegetarian, vegan, non_vegetarian, keto")
    variation: Optional[int] = Field(0, description="Variation index for shuffling/regenerating diverse meal plans")

    # Optional circumferences for US Navy body fat estimation (in cm)
    waist_cm: Optional[float] = None
    neck_cm: Optional[float] = None
    hip_cm: Optional[float] = None

class MacroBreakdown(BaseModel):
    protein_g: float
    carbs_g: float
    fat_g: float
    protein_calories: float
    carbs_calories: float
    fat_calories: float

class MealCalorieBudget(BaseModel):
    breakfast_kcal: float
    lunch_kcal: float
    dinner_kcal: float
    snacks_kcal: float

class HealthAssessmentResponse(BaseModel):
    bmi: float
    bmi_category: str
    bmi_status_color: str
    bmr: float
    tdee: float
    target_daily_calories: float
    calorie_adjustment: float
    body_fat_percentage: Optional[float] = None
    macro_targets: MacroBreakdown
    meal_budgets: MealCalorieBudget
    health_advice: str
