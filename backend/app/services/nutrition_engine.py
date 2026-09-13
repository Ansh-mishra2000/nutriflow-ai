import math
from typing import Optional, Dict
from app.schemas.health import (
    HealthAssessmentRequest,
    HealthAssessmentResponse,
    MacroBreakdown,
    MealCalorieBudget
)

class NutritionEngine:
    @staticmethod
    def calculate_bmi(weight_kg: float, height_cm: float) -> tuple[float, str, str]:
        """Calculates BMI, category, and badge color."""
        height_m = height_cm / 100.0
        bmi = round(weight_kg / (height_m ** 2), 2)
        
        if bmi < 18.5:
            category = "Underweight"
            color = "#3b82f6" # Blue
        elif 18.5 <= bmi < 25.0:
            category = "Normal / Healthy Weight"
            color = "#10b981" # Emerald Green
        elif 25.0 <= bmi < 30.0:
            category = "Overweight"
            color = "#f59e0b" # Amber
        elif 30.0 <= bmi < 35.0:
            category = "Obesity Class I"
            color = "#ef4444" # Red
        else:
            category = "Obesity Class II/III"
            color = "#b91c1c" # Dark Red
            
        return bmi, category, color

    @staticmethod
    def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
        """
        Mifflin-St Jeor Equation (Clinical Standard for Basal Metabolic Rate):
        Men:   10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) + 5
        Women: 10 * weight(kg) + 6.25 * height(cm) - 5 * age(y) - 161
        """
        base_bmr = (10.0 * weight_kg) + (6.25 * height_cm) - (5.0 * age)
        if gender.lower() == "male":
            bmr = base_bmr + 5
        else:
            bmr = base_bmr - 161
        return round(bmr, 1)

    @staticmethod
    def calculate_tdee(bmr: float, activity_level: str) -> float:
        """Calculates Total Daily Energy Expenditure based on physical activity multipliers."""
        multipliers = {
            "sedentary": 1.2,       # Little or no exercise / desk job
            "light": 1.375,         # Light exercise 1-3 days/week
            "moderate": 1.55,       # Moderate exercise 3-5 days/week
            "active": 1.725,        # Heavy exercise 6-7 days/week
            "very_active": 1.9      # Very heavy exercise / physical job
        }
        multiplier = multipliers.get(activity_level.lower(), 1.2)
        return round(bmr * multiplier, 1)

    @staticmethod
    def calculate_target_calories(tdee: float, goal: str, gender: str) -> tuple[float, float]:
        """Adjusts TDEE according to fitness goal with physiological safety minimums."""
        min_safe_calories = 1500.0 if gender.lower() == "male" else 1200.0
        
        if goal == "weight_loss":
            adjustment = -500.0 # Standard 0.5kg/week fat loss deficit
            target = max(tdee + adjustment, min_safe_calories)
        elif goal == "muscle_gain":
            adjustment = 350.0  # Clean bulking surplus
            target = tdee + adjustment
        else:
            adjustment = 0.0    # Maintenance
            target = tdee
            
        return round(target, 1), adjustment

    @staticmethod
    def calculate_macros(target_calories: float, weight_kg: float, goal: str) -> MacroBreakdown:
        """
        Calculates optimal macronutrient distribution:
        - Protein: 1.6-2.2g/kg based on goal (4 kcal/g)
        - Fats: 25% of daily calories (9 kcal/g)
        - Carbohydrates: Remaining calories (4 kcal/g)
        """
        if goal == "muscle_gain":
            protein_g_per_kg = 2.0
        elif goal == "weight_loss":
            protein_g_per_kg = 1.8
        else:
            protein_g_per_kg = 1.5

        protein_g = round(weight_kg * protein_g_per_kg, 1)
        protein_kcal = protein_g * 4.0

        # Fats at 25% of target calories
        fat_kcal = target_calories * 0.25
        fat_g = round(fat_kcal / 9.0, 1)

        # Remaining calories to carbohydrates
        carbs_kcal = max(target_calories - (protein_kcal + fat_kcal), 0)
        carbs_g = round(carbs_kcal / 4.0, 1)

        return MacroBreakdown(
            protein_g=protein_g,
            carbs_g=carbs_g,
            fat_g=fat_g,
            protein_calories=round(protein_kcal, 1),
            carbs_calories=round(carbs_kcal, 1),
            fat_calories=round(fat_kcal, 1)
        )

    @staticmethod
    def calculate_meal_budgets(target_calories: float) -> MealCalorieBudget:
        """Splits daily calorie budget across 4 structured meals."""
        return MealCalorieBudget(
            breakfast_kcal=round(target_calories * 0.25, 1), # 25%
            lunch_kcal=round(target_calories * 0.35, 1),     # 35%
            dinner_kcal=round(target_calories * 0.30, 1),    # 30%
            snacks_kcal=round(target_calories * 0.10, 1)     # 10%
        )

    @staticmethod
    def estimate_us_navy_body_fat(
        gender: str, height_cm: float, waist_cm: Optional[float],
        neck_cm: Optional[float], hip_cm: Optional[float]
    ) -> Optional[float]:
        """US Navy Body Fat formula (Gold standard tape measurement method)."""
        if not waist_cm or not neck_cm:
            return None
        try:
            if gender.lower() == "male":
                if waist_cm <= neck_cm:
                    return None
                bf = 495 / (1.0324 - 0.19077 * math.log10(waist_cm - neck_cm) + 0.15456 * math.log10(height_cm)) - 450
            else:
                if not hip_cm or (waist_cm + hip_cm) <= neck_cm:
                    return None
                bf = 495 / (1.29579 - 0.35004 * math.log10(waist_cm + hip_cm - neck_cm) + 0.22100 * math.log10(height_cm)) - 450
            return round(max(min(bf, 60.0), 3.0), 1)
        except Exception:
            return None

    @classmethod
    def evaluate_health(cls, req: HealthAssessmentRequest) -> HealthAssessmentResponse:
        bmi, bmi_cat, bmi_color = cls.calculate_bmi(req.weight_kg, req.height_cm)
        bmr = cls.calculate_bmr(req.weight_kg, req.height_cm, req.age, req.gender)
        tdee = cls.calculate_tdee(bmr, req.activity_level)
        target_cal, adj = cls.calculate_target_calories(tdee, req.goal, req.gender)
        macros = cls.calculate_macros(target_cal, req.weight_kg, req.goal)
        budgets = cls.calculate_meal_budgets(target_cal)
        body_fat = cls.estimate_us_navy_body_fat(req.gender, req.height_cm, req.waist_cm, req.neck_cm, req.hip_cm)

        if req.goal == "weight_loss":
            advice = f"Targeting a sustainable caloric deficit of 500 kcal/day to facilitate ~0.5kg weekly fat loss while preserving lean mass with {macros.protein_g}g daily protein."
        elif req.goal == "muscle_gain":
            advice = f"Targeting a clean lean bulk with a +350 kcal/day surplus and high protein ({macros.protein_g}g/day) to support muscle hypertrophy and recovery."
        else:
            advice = f"Maintaining energy equilibrium with balanced macronutrients to optimize daily vitality, metabolic rate, and cognitive performance."

        return HealthAssessmentResponse(
            bmi=bmi,
            bmi_category=bmi_cat,
            bmi_status_color=bmi_color,
            bmr=bmr,
            tdee=tdee,
            target_daily_calories=target_cal,
            calorie_adjustment=adj,
            body_fat_percentage=body_fat,
            macro_targets=macros,
            meal_budgets=budgets,
            health_advice=advice
        )
