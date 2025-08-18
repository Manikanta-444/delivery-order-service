from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database.connection import get_db
from app.models.order import DeliveryOrder, DeliveryItem
from app.schemas.order import DeliveryOrderCreate, DeliveryOrderUpdate, DeliveryOrder as DeliveryOrderSchema

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("/", response_model=DeliveryOrderSchema)
def create_order(order: DeliveryOrderCreate, db: Session = Depends(get_db)):
    # Create the order
    order_data = order.dict(exclude={'items'})
    db_order = DeliveryOrder(**order_data)
    db.add(db_order)
    db.flush()  # Get the order_id without committing

    # Create order items
    for item in order.items:
        db_item = DeliveryItem(**item.dict(), order_id=db_order.order_id)
        db.add(db_item)

    db.commit()
    db.refresh(db_order)
    return db_order


@router.get("/", response_model=List[DeliveryOrderSchema])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = db.query(DeliveryOrder).offset(skip).limit(limit).all()
    return orders


@router.get("/{order_id}", response_model=DeliveryOrderSchema)
def get_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    order = db.query(DeliveryOrder).filter(DeliveryOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put("/{order_id}", response_model=DeliveryOrderSchema)
def update_order(order_id: uuid.UUID, order_update: DeliveryOrderUpdate, db: Session = Depends(get_db)):
    order = db.query(DeliveryOrder).filter(DeliveryOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    for field, value in order_update.dict(exclude_unset=True).items():
        setattr(order, field, value)

    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}")
def delete_order(order_id: uuid.UUID, db: Session = Depends(get_db)):
    order = db.query(DeliveryOrder).filter(DeliveryOrder.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
