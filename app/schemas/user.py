# app/schemas/user.py
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    email: Optional[EmailStr] = None

    class Config:
        schema_extra = {
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "password": "strongpassword123"
            }
        }

class UserUpdate(BaseModel):
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    class Config:
        orm_mode = True
