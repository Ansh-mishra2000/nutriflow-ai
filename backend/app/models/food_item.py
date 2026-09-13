from sqlalchemy import Column, Integer, String, Float, Text
from app.db.session import Base

class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    category = Column(String, index=True, nullable=False) # breakfast, lunch, dinner, snack
    description = Column(Text, nullable=True)
    calories = Column(Float, nullable=False)
    protein_g = Column(Float, nullable=False)
    carbs_g = Column(Float, nullable=False)
    fat_g = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    diet_type = Column(String, default="any") # vegetarian, non_vegetarian, vegan, keto
    image_url = Column(String, nullable=True)
    prep_time_mins = Column(Integer, default=15)
    ingredients = Column(Text, nullable=True)
