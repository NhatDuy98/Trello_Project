from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

class BaseResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class LabelModel(BaseResponse):
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(..., min_length = 1, max_length = 100)

class LabelCreate(LabelModel):
    pass

class LabelUpdate(BaseResponse):
    label_name: str | None = Field(None, min_length = 1, max_length = 20)
    color: str = Field(None, min_length = 1, max_length = 100)

class LabelUpdated(LabelUpdate):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class Label(LabelModel):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class LabelResponse(BaseResponse):
    data: list[Label] = []