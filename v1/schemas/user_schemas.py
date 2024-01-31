from pydantic import BaseModel, Field, EmailStr, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.USER_NAME_PATTERN

class CamelCaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class PaginationModel(BaseModel):
    page: int = Field(..., gt = 0)
    limit: int = Field(..., gt = 0)
    totalRows: int

class UserModel(CamelCaseModel):
    first_name: str = Field(..., min_length= 1, max_length = 30, description = "must have 1 to 30 characters")
    last_name: str = Field(..., min_length = 1, max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(..., min_length = 1, max_length = 25, description = "email have at most 25 characters")

    @validator('first_name')
    @classmethod
    def validate_firstname(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('first name is invalid')
        return value
    
    @validator('last_name')
    @classmethod
    def validate_lastname(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('last name is invalid')
        return value

class UserCreate(UserModel):
    password: str = Field(..., min_length = 6, max_length = 18, description = "must have 6 to 18 characters")

class UserUpdate(UserModel):
    pass

class User(UserModel):
    id: int = Field(..., gt = 0)
    is_active: bool = Field(True)


class UpdateAPart(CamelCaseModel):
    first_name: str = Field(None, min_length = 1, max_length = 30, description = "must have 1 to 30 characters")
    last_name: str = Field(None, min_length = 1, max_length = 30, description = "last name have at most 30 characters")
    email: EmailStr = Field(None, min_length = 1, max_length = 25, description = "email have at most 25 characters")

    @validator('first_name')
    @classmethod
    def validate_firstname(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('first name is invalid')
        return value
    
    @validator('last_name')
    @classmethod
    def validate_lastname(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('last name is invalid')
        return value

class UserUpdateAPart(UpdateAPart):
    id: int = Field(..., gt = 0)
    is_active: bool = Field(True)
    

class UserResponse(BaseModel):
    data: list[User] = []
    pagination: PaginationModel