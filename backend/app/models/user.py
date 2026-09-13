from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from datetime import datetime, timezone
from app.db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Health Profile Fields
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True) # male / female
    height_cm = Column(Float, nullable=True)
    weight_kg = Column(Float, nullable=True)
    activity_level = Column(String, default="sedentary") # sedentary, light, moderate, active, very_active
    goal = Column(String, default="maintenance") # weight_loss, maintenance, muscle_gain
    diet_preference = Column(String, default="any") # any, vegetarian, vegan, non_vegetarian, keto

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
