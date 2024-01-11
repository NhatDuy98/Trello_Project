from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class PaginationModel(BaseModel):
    page: int
    limit: int
    totalRows: int

class BoardModel(ModelResponse):
    board_name: str = Field(..., min_length = 1, max_length = 45, description = 'between 1 to 45 characters')
    description: str | None = Field(None, max_length = 255, description = 'too much characters')

class BoardCreate(BoardModel):
    pass

class BoardUpdate(ModelResponse):
    board_name: str | None = Field(None, min_length = 1, max_length = 45, description = 'between 1 to 45 charactes')
    description: str | None = Field(None, min_length = 1, max_length = 255, description = 'too much characters')

class BoardUpdated(BoardUpdate):
    id: int = Field(..., gt = 0)
    work_space_id: int = Field(..., gt = 0)

class Board(BoardModel):
    id: int = Field(..., gt = 0)
    work_space_id: int = Field(..., gt = 0)

class BoardResponse(BaseModel):
    data: list[Board] = []
    pagination: PaginationModel