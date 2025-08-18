from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid


class AddressBase(BaseModel):
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str = "India"
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: bool = False


class AddressCreate(AddressBase):
    customer_id: uuid.UUID


class AddressUpdate(BaseModel):
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[Decimal] = None
    longitude: Optional[Decimal] = None
    is_default: Optional[bool] = None


class Address(AddressBase):
    address_id: uuid.UUID
    customer_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True
