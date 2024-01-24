from pydantic import BaseModel, Field, EmailStr
from pydantic.alias_generators import to_camel
from datetime import datetime

class ModelResponse(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = to_camel

class UserModel(ModelResponse):
    first_name: str = Field(..., max_length = 30, description = "first name have at most 30 characters")
    last_name: str = Field(..., max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(..., max_length = 25, description = "email have at most 25 characters")

class UserCreate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")

class UserUpdate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")
    is_delete: bool = Field(False)
    updated_at: datetime = Field(datetime.now())
    deleted_at: datetime = Field(None)

class User(UserModel):
    id: int = Field(..., gt = 0)
    is_active: bool = Field(True)