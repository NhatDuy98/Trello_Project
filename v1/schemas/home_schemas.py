from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.alias_generators import to_camel
from datetime import datetime
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.USER_NAME_PATTERN

class ModelResponse(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = to_camel

class UserModel(ModelResponse):
    first_name: str = Field(..., min_length = 1, max_length = 30, description = "first name have at most 30 characters")
    last_name: str = Field(..., min_length = 1, max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(..., min_length = 1, max_length = 25, description = "email have at most 25 characters")

    @validator("first_name")
    @classmethod
    def validate_first_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError("first name is invalid")
        return value
    
    @validator("last_name")
    @classmethod
    def validate_last_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError("last name is invalid")
        return value

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