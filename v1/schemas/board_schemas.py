from pydantic import BaseModel, Field, validator
from pydantic.alias_generators import to_camel
from v1.schemas import pattern_schemas

name_pattern = pattern_schemas.NAME_PATTERN


class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class PaginationModel(BaseModel):
    page: int = Field(..., gt = 0)
    limit: int = Field(..., gt = 0)
    totalRows: int

class BoardModel(ModelResponse):
    board_name: str = Field(..., min_length = 1, max_length = 45, description = 'between 1 to 45 characters')
    description: str | None = Field(None, max_length = 255, description = 'too much characters')

    @validator('board_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('name is invalid')
        return value

class BoardCreate(BoardModel):
    pass

class BoardUpdate(ModelResponse):
    board_name: str | None = Field(None, min_length = 1, max_length = 45, description = 'between 1 to 45 charactes')
    description: str | None = Field(None, min_length = 1, max_length = 255, description = 'too much characters')
    
    @validator('board_name')
    @classmethod
    def validate_name(cls, value):
        if not bool(name_pattern.fullmatch(value)):
            raise ValueError('name is invalid')
        return value

class BoardUpdated(BoardUpdate):
    id: int = Field(..., gt = 0)
    work_space_id: int = Field(..., gt = 0)

class Board(BoardModel):
    id: int = Field(..., gt = 0)
    work_space_id: int = Field(..., gt = 0)

class BoardResponse(BaseModel):
    data: list[Board] = []
    pagination: PaginationModel