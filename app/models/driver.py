from sqlalchemy import Column, String, Boolean, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database.connection import Base


class Driver(Base):
    __tablename__ = 'drivers'
    __table_args__ = {'schema': 'delivery_order_service'}

    driver_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    license_number = Column(String(50), unique=True, nullable=False)
    vehicle_capacity_kg = Column(Numeric(8, 2), default=500.00)
    vehicle_type = Column(String(50), default='VAN')
    is_available = Column(Boolean, default=True)
    current_latitude = Column(Numeric(10, 8))
    current_longitude = Column(Numeric(11, 8))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
