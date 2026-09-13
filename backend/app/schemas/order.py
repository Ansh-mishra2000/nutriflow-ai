from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class OrderItemCreate(BaseModel):
    food_item_id: int
    quantity: int = Field(1, ge=1)

class OrderCreate(BaseModel):
    customer_name: str
    delivery_address: str
    phone_number: str
    items: List[OrderItemCreate]

class OrderItemResponse(BaseModel):
    id: int
    food_item_id: int
    food_name: str
    quantity: int
    price_per_item: float
    calories_per_item: float
    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    customer_name: str
    delivery_address: str
    phone_number: str
    total_amount: float
    total_calories: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse] = []
    model_config = ConfigDict(from_attributes=True)

class OrderStatusUpdate(BaseModel):
    status: str
