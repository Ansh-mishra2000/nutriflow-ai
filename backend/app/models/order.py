from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db.session import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String, nullable=False)
    delivery_address = Column(Text, nullable=False)
    phone_number = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    total_calories = Column(Float, nullable=False)
    status = Column(String, default="PLACED") # PLACED, PREPARING, OUT_FOR_DELIVERY, DELIVERED
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    food_item_id = Column(Integer, ForeignKey("food_items.id"), nullable=False)
    food_name = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    price_per_item = Column(Float, nullable=False)
    calories_per_item = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
