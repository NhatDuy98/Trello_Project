from pydantic import BaseModel, Field
from datetime import datetime
from pydantic.alias_generators import to_camel

class ModelConfig(BaseModel):
    class Config:
        from_attributes = True
        alias_generator = to_camel

class PaginationModel(BaseModel):
    page: int = Field(None)
    limit: int = Field(None)
    totalRows: int = Field(None)

class WorkSpaceModel(ModelConfig):
    work_space_name: str = Field(..., min_length = 1, max_length = 45, description = "name must have 1 to 45 characters")
    desciption: str | None = Field(None, max_length = 255, description = "too long")

class WorkSpaceCreate(WorkSpaceModel):
    pass

class WorkSpaceUpdate(ModelConfig):
    work_space_name: str = Field(None, min_length = 1, max_length = 45, description = "name must have 1 to 45 characters")
    desciption: str | None = Field(None, max_length = 255, description = "too long")

class WorkSpaceUpdated(WorkSpaceUpdate):
    id: int = Field(..., gt = 0)
    user_id: int = Field(..., gt = 0)

class WorkSpace(WorkSpaceModel):
    id: int = Field(..., gt = 0)
    user_id: int = Field(..., gt = 0)


class WorkSpaceResponse(BaseModel):
    data: list[WorkSpace] = []
    pagination: PaginationModel

