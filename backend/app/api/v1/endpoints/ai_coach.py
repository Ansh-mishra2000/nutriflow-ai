from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()

class AICoachQuery(BaseModel):
    user_goal: str
    daily_calories: float
    question: str
    diet_preference: Optional[str] = "any"

class AICoachResponse(BaseModel):
    answer: str
    ai_provider: str

@router.post("/ask", response_model=AICoachResponse, summary="AI Nutritionist Chat & Recipe Advice")
def ask_ai_nutritionist(query: AICoachQuery):
    """
    Provides intelligent nutrition and recipe customization coaching.
    If Google Gemini API key is configured, provides live LLM response; otherwise uses rule-based expert engine.
    """
    gemini_key = os.getenv("GEMINI_API_KEY", "")
    if gemini_key:
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            prompt = f"""You are NutriFlow AI, an elite clinical nutritionist and chef.
User Context:
- Goal: {query.user_goal}
- Caloric Target: {query.daily_calories} kcal/day
- Diet Preference: {query.diet_preference}
User Question: {query.question}

Provide clear, encouraging, evidence-based nutritional guidance and delicious cooking/prep tips."""
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return AICoachResponse(answer=response.text, ai_provider="Google Gemini 2.5 Flash")
        except Exception as e:
            pass

    # Built-in High Quality Expert Knowledge Fallback
    fallback_tips = {
        "weight_loss": "To optimize fat loss without hunger, prioritize high-volume, low-calorie foods such as leafy greens, cruciferous vegetables, and lean proteins (chicken breast, egg whites, tofu). Drink 500ml water before every meal.",
        "muscle_gain": "To support clean hypertrophy, distribute your protein evenly into 4 meals of 30-45g each, consume complex carbohydrates (oats, brown rice, sweet potatoes) around your training window, and ensure 7-8 hours of sleep.",
        "maintenance": "For sustained energy and metabolic health, focus on the 80/20 rule: 80% whole nutrient-dense foods and 20% flexibility, keeping hydration high and maintaining daily step counts."
    }
    tip = fallback_tips.get(query.user_goal.lower(), fallback_tips["maintenance"])
    answer = f"**Nutritional Strategy for {query.user_goal.upper()} ({query.daily_calories} kcal/day):**\n\n{tip}\n\n*Regarding your question:* '{query.question}' — Be sure to stick to whole unprocessed ingredients, track your sodium intake, and balance macro ratios across breakfast, lunch, and dinner."
    return AICoachResponse(answer=answer, ai_provider="NutriFlow Built-in Expert Engine")
