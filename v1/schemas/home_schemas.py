from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class Config:
    from_attributes = True
    # orm_mode = True

class UserModel(BaseModel):
    firstName: str = Field(..., max_length = 30, description = "first name have at most 30 characters")
    lastName: str = Field(..., max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(..., max_length = 25, description = "email have at most 25 characters")

class UserCreate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")

class UserUpdate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")
    isDelete: bool = Field(False)
    updatedAt: datetime = Field(datetime.now())
    deletedAt: datetime = Field(None)

class User(UserModel, Config):
    id: int = Field(..., gt = 0)
    isActive: bool = Field(True)