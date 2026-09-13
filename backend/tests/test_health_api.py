import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_db

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_calculate_health_endpoint():
    payload = {
        "age": 24,
        "gender": "male",
        "height_cm": 178.0,
        "weight_kg": 74.0,
        "activity_level": "moderate",
        "goal": "muscle_gain",
        "diet_preference": "non_vegetarian"
    }
    response = client.post("/api/v1/health/calculate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "bmi" in data
    assert data["bmi"] == 23.36
    assert "bmr" in data
    assert "tdee" in data
    assert data["target_daily_calories"] > data["tdee"]
    assert "macro_targets" in data
    assert data["macro_targets"]["protein_g"] > 0

def test_day_plan_recommendation_endpoint():
    payload = {
        "age": 26,
        "gender": "female",
        "height_cm": 165.0,
        "weight_kg": 62.0,
        "activity_level": "light",
        "goal": "weight_loss",
        "diet_preference": "vegetarian"
    }
    response = client.post("/api/v1/recommendations/day-plan", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "meals" in data
    assert len(data["meals"]) == 4
    assert "workout" in data
    assert data["workout"]["title"] is not None
