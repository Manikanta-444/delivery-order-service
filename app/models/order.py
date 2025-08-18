from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Numeric, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
from app.database.connection import Base


class DeliveryOrder(Base):
    __tablename__ = 'delivery_orders'
    __table_args__ = {'schema': 'delivery_order_service'}

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('delivery_order_service.customers.customer_id'), nullable=False)
    pickup_address_id = Column(UUID(as_uuid=True), ForeignKey('delivery_order_service.addresses.address_id'))
    delivery_address_id = Column(UUID(as_uuid=True), ForeignKey('delivery_order_service.addresses.address_id'))
    order_status = Column(String(50), default='PENDING')
    priority_level = Column(Integer, default=1)
    requested_delivery_time = Column(DateTime)
    estimated_delivery_time = Column(DateTime)
    actual_delivery_time = Column(DateTime)
    total_weight = Column(Numeric(8, 2))
    total_volume = Column(Numeric(8, 2))
    special_instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="orders")
    pickup_address = relationship("Address", foreign_keys=[pickup_address_id], back_populates="pickup_orders")
    delivery_address = relationship("Address", foreign_keys=[delivery_address_id], back_populates="delivery_orders")
    items = relationship("DeliveryItem", back_populates="order")


class DeliveryItem(Base):
    __tablename__ = 'delivery_items'
    __table_args__ = {'schema': 'delivery_order_service'}

    item_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey('delivery_order_service.delivery_orders.order_id'), nullable=False)
    item_name = Column(String(255), nullable=False)
    quantity = Column(Integer, default=1)
    weight = Column(Numeric(8, 2))
    dimensions = Column(String(100))
    fragile = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("DeliveryOrder", back_populates="items")
