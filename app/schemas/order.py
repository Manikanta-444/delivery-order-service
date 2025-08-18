from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
import uuid


class DeliveryItemBase(BaseModel):
    item_name: str
    quantity: int = 1
    weight: Optional[Decimal] = None
    dimensions: Optional[str] = None
    fragile: bool = False


class DeliveryItemCreate(DeliveryItemBase):
    pass


class DeliveryItem(DeliveryItemBase):
    item_id: uuid.UUID
    order_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class DeliveryOrderBase(BaseModel):
    pickup_address_id: Optional[uuid.UUID] = None
    delivery_address_id: uuid.UUID
    priority_level: int = 1
    requested_delivery_time: Optional[datetime] = None
    total_weight: Optional[Decimal] = None
    total_volume: Optional[Decimal] = None
    special_instructions: Optional[str] = None


class DeliveryOrderCreate(DeliveryOrderBase):
    customer_id: uuid.UUID
    items: List[DeliveryItemCreate] = []


class DeliveryOrderUpdate(BaseModel):
    order_status: Optional[str] = None
    estimated_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None


class DeliveryOrder(DeliveryOrderBase):
    order_id: uuid.UUID
    customer_id: uuid.UUID
    order_status: str
    estimated_delivery_time: Optional[datetime] = None
    actual_delivery_time: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    items: List[DeliveryItem] = []

    class Config:
        from_attributes = True
