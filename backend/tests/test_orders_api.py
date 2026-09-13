import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.init_db import init_db

@pytest.fixture(autouse=True)
def setup_db():
    init_db()

client = TestClient(app)

def test_order_and_delivery_lifecycle():
    # 1. Fetch available meals
    catalog_res = client.get("/api/v1/catalog/meals")
    assert catalog_res.status_code == 200
    meals = catalog_res.json()
    assert len(meals) > 0
    meal1 = meals[0]

    # 2. Create order
    order_payload = {
        "customer_name": "Ansh Mishra",
        "delivery_address": "Sector 16C, Dwarka, Delhi",
        "phone_number": "+91-9876543210",
        "items": [
            {"food_item_id": meal1["id"], "quantity": 2}
        ]
    }
    create_res = client.post("/api/v1/orders/", json=order_payload)
    assert create_res.status_code == 200
    order = create_res.json()
    assert order["status"] == "PLACED"
    assert order["total_amount"] == round(meal1["price"] * 2, 2)
    assert order["total_calories"] == round(meal1["calories"] * 2, 1)
    order_id = order["id"]

    # 3. Track order
    get_res = client.get(f"/api/v1/orders/{order_id}")
    assert get_res.status_code == 200
    assert get_res.json()["status"] == "PLACED"

    # 4. Advance status -> PREPARING
    adv1 = client.post(f"/api/v1/orders/{order_id}/advance-status")
    assert adv1.status_code == 200
    assert adv1.json()["status"] == "PREPARING"

    # 5. Advance status -> OUT_FOR_DELIVERY
    adv2 = client.post(f"/api/v1/orders/{order_id}/advance-status")
    assert adv2.status_code == 200
    assert adv2.json()["status"] == "OUT_FOR_DELIVERY"

    # 6. Advance status -> DELIVERED
    adv3 = client.post(f"/api/v1/orders/{order_id}/advance-status")
    assert adv3.status_code == 200
    assert adv3.json()["status"] == "DELIVERED"
