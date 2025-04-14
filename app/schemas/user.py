# app/schemas/user.py
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str = None
    email: EmailStr = None
    password: str = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True
