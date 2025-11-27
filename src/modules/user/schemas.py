from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
import re



class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    organization_name: str
    position: str
    department: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserRegister(UserBase):
    password: Annotated[str, Field(min_length=8)]

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('Пароль должен содержать заглавные буквы')
        if not re.search(r'[a-z]', v):
            raise ValueError('Пароль должен содержать строчные буквы')
        if not re.search(r'\d', v):
            raise ValueError('Пароль должен содержать цифры')
        return v

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v: str) -> str:
        if len(v.split()) < 2:
            raise ValueError('Укажите имя и фамилию')
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str