from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

class ModelResponse(BaseModel):
    class Config:
        alias_generator = to_camel
        from_attributes = True

class ListWorkModel(ModelResponse):
    list_work_name: str = Field(..., min_length = 1, max_length = 45)

class ListWorkCreate(ListWorkModel):
    pass

class ListWorkUpdate(ListWorkModel):
    pass

class ListWork(ListWorkModel):
    id: int = Field(..., gt = 0)
    board_id: int = Field(..., gt = 0)

class ListWorkResponse(ModelResponse):
    data: list[ListWork] = []