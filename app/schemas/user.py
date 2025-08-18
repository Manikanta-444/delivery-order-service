from pydantic import BaseModel, EmailStr, constr
from enum import Enum
from typing import Optional
import uuid

class UserRole(str, Enum):
    CUSTOMER = "customer"
    DISPATCHER = "dispatcher"

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: constr(min_length=8)
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    user_id: uuid.UUID
    is_active: bool
    role: str

    class Config:
        from_attributes = True
