import pytest
from app.services.nutrition_engine import NutritionEngine
from app.schemas.health import HealthAssessmentRequest

def test_bmi_calculation():
    # Weight: 70kg, Height: 175cm -> BMI = 70 / (1.75^2) = 22.86 (Normal)
    bmi, category, color = NutritionEngine.calculate_bmi(70.0, 175.0)
    assert bmi == 22.86
    assert category == "Normal / Healthy Weight"
    assert color == "#10b981"

    # Overweight test
    bmi_over, cat_over, _ = NutritionEngine.calculate_bmi(90.0, 175.0)
    assert bmi_over == 29.39
    assert cat_over == "Overweight"

def test_bmr_mifflin_st_jeor():
    # Male: 25 years old, 75kg, 180cm
    # BMR = (10*75) + (6.25*180) - (5*25) + 5 = 750 + 1125 - 125 + 5 = 1755.0
    bmr_male = NutritionEngine.calculate_bmr(75.0, 180.0, 25, "male")
    assert bmr_male == 1755.0

    # Female: 25 years old, 60kg, 165cm
    # BMR = (10*60) + (6.25*165) - (5*25) - 161 = 600 + 1031.25 - 125 - 161 = 1345.25 -> 1345.2 or 1345.3
    bmr_female = NutritionEngine.calculate_bmr(60.0, 165.0, 25, "female")
    assert 1345.0 <= bmr_female <= 1346.0

def test_tdee_and_goal_calories():
    bmr = 1755.0
    tdee = NutritionEngine.calculate_tdee(bmr, "moderate")
    assert tdee == round(1755.0 * 1.55, 1) # 2720.2 or 2720.3

    # Weight loss deficit
    target_loss, adj_loss = NutritionEngine.calculate_target_calories(tdee, "weight_loss", "male")
    assert adj_loss == -500.0
    assert target_loss == round(tdee - 500.0, 1)

def test_meal_calorie_budgets():
    budgets = NutritionEngine.calculate_meal_budgets(2000.0)
    assert budgets.breakfast_kcal == 500.0 # 25%
    assert budgets.lunch_kcal == 700.0     # 35%
    assert budgets.dinner_kcal == 600.0    # 30%
    assert budgets.snacks_kcal == 200.0    # 10%
    assert sum([budgets.breakfast_kcal, budgets.lunch_kcal, budgets.dinner_kcal, budgets.snacks_kcal]) == 2000.0
