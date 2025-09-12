from app.apis.users.models import UserRole
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr  

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None

class UserRead(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        from_attributes = True  