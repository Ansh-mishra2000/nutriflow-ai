from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.food_item import FoodItem
from app.schemas.order import OrderCreate, OrderResponse

VALID_STATUS_FLOW = ["PLACED", "PREPARING", "OUT_FOR_DELIVERY", "DELIVERED"]

class OrderService:
    @staticmethod
    def create_order(db: Session, order_in: OrderCreate, user_id: Optional[int] = None) -> Order:
        if not order_in.items:
            raise HTTPException(status_code=400, detail="Cannot create an empty order.")

        total_amount = 0.0
        total_calories = 0.0
        order_items = []

        for item_in in order_in.items:
            food = db.query(FoodItem).filter(FoodItem.id == item_in.food_item_id).first()
            if not food:
                raise HTTPException(status_code=404, detail=f"Food item with id {item_in.food_item_id} not found.")

            item_total_price = food.price * item_in.quantity
            item_total_cals = food.calories * item_in.quantity
            total_amount += item_total_price
            total_calories += item_total_cals

            order_item = OrderItem(
                food_item_id=food.id,
                food_name=food.name,
                quantity=item_in.quantity,
                price_per_item=food.price,
                calories_per_item=food.calories
            )
            order_items.append(order_item)

        order = Order(
            user_id=user_id,
            customer_name=order_in.customer_name,
            delivery_address=order_in.delivery_address,
            phone_number=order_in.phone_number,
            total_amount=round(total_amount, 2),
            total_calories=round(total_calories, 1),
            status="PLACED",
            items=order_items
        )

        db.add(order)
        db.commit()
        db.refresh(order)
        return order

    @staticmethod
    def get_order_by_id(db: Session, order_id: int) -> Order:
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail=f"Order #{order_id} not found.")
        return order

    @staticmethod
    def advance_delivery_status(db: Session, order_id: int) -> Order:
        order = OrderService.get_order_by_id(db, order_id)
        current_idx = VALID_STATUS_FLOW.index(order.status) if order.status in VALID_STATUS_FLOW else 0
        if current_idx < len(VALID_STATUS_FLOW) - 1:
            order.status = VALID_STATUS_FLOW[current_idx + 1]
            db.commit()
            db.refresh(order)
        return order
