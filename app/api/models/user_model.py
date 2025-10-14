# app/api/models/user_model.py
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, String, Float
from app.configurations.database import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    mobile_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    current_role = Column(String, nullable=True)
    total_experience = Column(Float, default=0.0)

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    mobile_number: str
    password: str
    current_role: Optional[str] = None
    total_experience: Optional[float] = 0.0

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile_number: Optional[str] = None
    password: Optional[str] = None
    current_role: Optional[str] = None
    total_experience: Optional[float] = None

    class Config:
        from_attributes = True
