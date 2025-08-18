from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.connection import Base


class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'schema': 'delivery_order_service'}

    address_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('delivery_order_service.customers.customer_id'), nullable=False)
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    postal_code = Column(String(20), nullable=False)
    country = Column(String(100), default='India')
    latitude = Column(Numeric(10, 8))
    longitude = Column(Numeric(11, 8))
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="addresses")
    pickup_orders = relationship("DeliveryOrder", foreign_keys="DeliveryOrder.pickup_address_id",
                                 back_populates="pickup_address")
    delivery_orders = relationship("DeliveryOrder", foreign_keys="DeliveryOrder.delivery_address_id",
                                   back_populates="delivery_address")
