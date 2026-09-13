from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services.order_service import OrderService
from app.models.order import Order

router = APIRouter()

@router.post("/", response_model=OrderResponse, summary="Place a Calorie-Tracked Food Delivery Order")
def create_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """
    Places an order for recommended meals, calculating real-time total calories and billing amount.
    """
    return OrderService.create_order(db=db, order_in=order_in)

@router.get("/{order_id}", response_model=OrderResponse, summary="Get Order & Delivery Tracking Status")
def get_order(order_id: int, db: Session = Depends(get_db)):
    """
    Fetches order details and real-time delivery status:
    `PLACED` -> `PREPARING` -> `OUT_FOR_DELIVERY` -> `DELIVERED`
    """
    return OrderService.get_order_by_id(db=db, order_id=order_id)

@router.post("/{order_id}/advance-status", response_model=OrderResponse, summary="Simulate Delivery Driver Progression")
def advance_delivery_status(order_id: int, db: Session = Depends(get_db)):
    """
    Advances delivery lifecycle to simulate real-time driver progression.
    """
    return OrderService.advance_delivery_status(db=db, order_id=order_id)

@router.get("/", response_model=List[OrderResponse], summary="List Recent Orders")
def list_orders(limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Order).order_by(Order.created_at.desc()).limit(limit).all()
