from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.food_item import FoodItem
from app.schemas.health import HealthAssessmentResponse
from app.schemas.meal import (
    FoodItemResponse,
    MealRecommendation,
    WorkoutRecommendation,
    DayPlanResponse
)

WORKOUT_ROUTINES = {
    "weight_loss": {
        "title": "Metabolic Fat-Loss & High-Intensity Conditioning (HIIT)",
        "type": "HIIT + Resistance",
        "intensity": "High",
        "duration_mins": 45,
        "description": "Combines compound movements and short cardio intervals to maximize EPOC (Excess Post-Exercise Oxygen Consumption) and preserve lean muscle mass during a calorie deficit.",
        "exercises": [
            "1. Kettlebell Goblet Squats (4 sets x 12 reps)",
            "2. Dumbbell Romanian Deadlifts (4 sets x 10 reps)",
            "3. High-Intensity Mountain Climbers (4 sets x 40 seconds)",
            "4. Push-ups to Renegade Row (3 sets x 10 reps)",
            "5. Battle Ropes or Sprint Intervals (5 rounds x 30s ON / 30s OFF)",
            "6. Hanging Knee Raises or Ab Planks (3 sets x 60 seconds)"
        ]
    },
    "muscle_gain": {
        "title": "Hypertrophy & Strength Progressive Overload Routine",
        "type": "Hypertrophy Resistance",
        "intensity": "Moderate-High",
        "duration_mins": 55,
        "description": "Focused on multi-joint compound lifts with progressive overload and optimal rest intervals to stimulate mechanical tension and muscle protein synthesis.",
        "exercises": [
            "1. Barbell Back Squats (4 sets x 6-8 reps, 2 min rest)",
            "2. Barbell Bench Press (4 sets x 6-8 reps, 2 min rest)",
            "3. Barbell Bent-Over Rows (4 sets x 8-10 reps)",
            "4. Overhead Dumbbell Shoulder Press (3 sets x 10-12 reps)",
            "5. Incline Dumbbell Curls superset with Tricep Rope Pushdowns (3 sets x 12 reps)",
            "6. Hanging Leg Raises (3 sets x 15 reps)"
        ]
    },
    "maintenance": {
        "title": "Functional Total Body Mobility & Athletic Fitness",
        "type": "Functional Strength & Cardio",
        "intensity": "Moderate",
        "duration_mins": 45,
        "description": "Balanced total-body training focusing on joint mobility, core stability, cardiovascular endurance, and functional strength.",
        "exercises": [
            "1. Dumbbell Bulgarian Split Squats (3 sets x 10 reps per leg)",
            "2. Pull-ups or Lat Pulldowns (4 sets x 10 reps)",
            "3. Flat Dumbbell Chest Press (3 sets x 10 reps)",
            "4. Kettlebell Swings (4 sets x 15 reps)",
            "5. Side Plank with Hip Abduction (3 sets x 45s per side)",
            "6. 20-minute Zone 2 Cardio (Incline Walking / Cycling at 65% Max HR)"
        ]
    }
}

class RecommenderService:
    @staticmethod
    def get_meal_for_category(
        db: Session,
        category: str,
        target_calories: float,
        diet_preference: Optional[str] = "any",
        variation: int = 0
    ) -> MealRecommendation:
        query = db.query(FoodItem).filter(FoodItem.category == category.lower())

        if diet_preference and diet_preference.lower() not in ["any", "all"]:
            pref = diet_preference.lower()
            if pref == "vegetarian":
                query = query.filter(FoodItem.diet_type.in_(["vegetarian", "vegan"]))
            elif pref == "vegan":
                query = query.filter(FoodItem.diet_type == "vegan")
            elif pref == "keto":
                query = query.filter(FoodItem.diet_type == "keto")
            elif pref == "non_vegetarian":
                query = query.filter(FoodItem.diet_type.in_(["non_vegetarian", "vegetarian", "vegan"]))

        items = query.all()
        if not items:
            # Fallback to all items in category if strict filter yields no results
            items = db.query(FoodItem).filter(FoodItem.category == category.lower()).all()

        if not items:
            # Generic fallback
            fallback_item = FoodItem(
                id=0,
                name=f"Custom Balanced {category.capitalize()} Bowl",
                category=category.lower(),
                description="Nutrient dense whole foods customized to your calorie target.",
                calories=target_calories,
                protein_g=round(target_calories * 0.25 / 4, 1),
                carbs_g=round(target_calories * 0.50 / 4, 1),
                fat_g=round(target_calories * 0.25 / 9, 1),
                price=199.0,
                diet_type="any"
            )
            return MealRecommendation(
                category=category.capitalize(),
                target_calories=target_calories,
                recommended_food=FoodItemResponse.model_validate(fallback_item),
                calorie_variance=0.0,
                alternative_foods=[]
            )

        # Sort items by proximity to target calories and cycle through permutations with variation
        sorted_items = sorted(items, key=lambda item: abs(item.calories - target_calories))
        idx = variation % len(sorted_items)
        primary_choice = sorted_items[idx]
        alternatives = [item for i, item in enumerate(sorted_items) if i != idx][:2]

        return MealRecommendation(
            category=category.capitalize(),
            target_calories=target_calories,
            recommended_food=FoodItemResponse.model_validate(primary_choice),
            calorie_variance=round(primary_choice.calories - target_calories, 1),
            alternative_foods=[FoodItemResponse.model_validate(alt) for alt in alternatives]
        )

    @classmethod
    def generate_day_plan(
        cls,
        db: Session,
        health: HealthAssessmentResponse,
        goal: str,
        diet_preference: Optional[str] = "any",
        variation: int = 0
    ) -> DayPlanResponse:
        breakfast = cls.get_meal_for_category(db, "breakfast", health.meal_budgets.breakfast_kcal, diet_preference, variation)
        lunch = cls.get_meal_for_category(db, "lunch", health.meal_budgets.lunch_kcal, diet_preference, variation * 2 + 1)
        dinner = cls.get_meal_for_category(db, "dinner", health.meal_budgets.dinner_kcal, diet_preference, variation * 3 + 2)
        snack = cls.get_meal_for_category(db, "snack", health.meal_budgets.snacks_kcal, diet_preference, variation * 4 + 3)

        meals = [breakfast, lunch, dinner, snack]
        total_calories = sum(m.recommended_food.calories for m in meals)
        total_protein = sum(m.recommended_food.protein_g for m in meals)
        total_carbs = sum(m.recommended_food.carbs_g for m in meals)
        total_fat = sum(m.recommended_food.fat_g for m in meals)

        workout_data = WORKOUT_ROUTINES.get(goal.lower(), WORKOUT_ROUTINES["maintenance"])
        workout = WorkoutRecommendation(**workout_data)

        return DayPlanResponse(
            health_summary={
                "bmi": health.bmi,
                "bmi_category": health.bmi_category,
                "bmi_status_color": health.bmi_status_color,
                "bmr": health.bmr,
                "tdee": health.tdee,
                "target_daily_calories": health.target_daily_calories,
                "calorie_adjustment": health.calorie_adjustment,
                "body_fat_percentage": health.body_fat_percentage,
                "health_advice": health.health_advice
            },
            total_plan_calories=round(total_calories, 1),
            total_plan_protein=round(total_protein, 1),
            total_plan_carbs=round(total_carbs, 1),
            total_plan_fat=round(total_fat, 1),
            meals=meals,
            workout=workout
        )
