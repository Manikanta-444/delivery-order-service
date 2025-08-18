from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid


class DriverBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    license_number: str
    vehicle_capacity_kg: Decimal = Decimal('500.00')
    vehicle_type: str = 'VAN'
    is_available: bool = True
    current_latitude: Optional[Decimal] = None
    current_longitude: Optional[Decimal] = None


class DriverCreate(DriverBase):
    pass


class DriverUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    is_available: Optional[bool] = None
    current_latitude: Optional[Decimal] = None
    current_longitude: Optional[Decimal] = None


class Driver(DriverBase):
    driver_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
