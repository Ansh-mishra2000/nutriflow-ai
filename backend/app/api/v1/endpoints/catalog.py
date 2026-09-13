from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.food_item import FoodItem
from app.schemas.meal import FoodItemResponse

router = APIRouter()

@router.get("/meals", response_model=List[FoodItemResponse], summary="Get Food & Meal Catalog")
def get_meal_catalog(
    category: Optional[str] = Query(None, description="Filter by meal category: breakfast, lunch, dinner, snack"),
    diet_type: Optional[str] = Query(None, description="Filter by diet: vegetarian, vegan, non_vegetarian, keto"),
    db: Session = Depends(get_db)
):
    query = db.query(FoodItem)
    if category:
        query = query.filter(FoodItem.category == category.lower())
    if diet_type and diet_type.lower() != "any":
        query = query.filter(FoodItem.diet_type == diet_type.lower())
    return query.all()

@router.get("/meals/{item_id}", response_model=FoodItemResponse, summary="Get Single Meal Details")
def get_meal_item(item_id: int, db: Session = Depends(get_db)):
    return db.query(FoodItem).filter(FoodItem.id == item_id).first()
