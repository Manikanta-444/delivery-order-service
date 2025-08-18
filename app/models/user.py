from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.database.connection import Base

class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'delivery_order_service'}

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    email = Column(String(255))
    is_active = Column(String(100), default=True)
    role = Column(String(50), default="dispatcher")
    created_at = Column(DateTime, default=datetime.utcnow)
