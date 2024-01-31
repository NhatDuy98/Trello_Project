from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db
from core.config import get_settings
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import work_spaces
from v1.services import work_space_service
from v1.schemas import  work_space_schemas

settings = get_settings()

work_ep = settings.END_POINT_WORK_SPACE

router = APIRouter(
    tags = ["WorkSpace"],
    responses = {404: {"description": "WorkSpace not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(f'/{work_ep}', response_model = work_space_schemas.WorkSpaceResponse, status_code = status.HTTP_200_OK)
def get_all_work_spaces(
    db: db_dependency,
    page: Annotated[int, Query()] = 1,
    limit: Annotated[int, Query] = 5,
    sort_by: Annotated[str, Query()] = None,
    sort_desc: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None
):
    work_spaces = work_space_service.get_all_with_pagination(
        db = db,
        page = page,
        limit = limit,
        sort_by = sort_by,
        sort_desc = sort_desc,
        search = search
    )
    return work_spaces

@router.post('/{user_id}'f'/{work_ep}', response_model = work_space_schemas.WorkSpace, status_code = status.HTTP_201_CREATED)
def create_work_space(
    db: db_dependency,
    user_id: Annotated[int, Path(...)],
    work_space: Annotated[work_space_schemas.WorkSpaceCreate, Body(...)]
):
    work_space_response = work_space_service.create_work_space(
        db = db,
        user_id = user_id,
        work_space = work_space
    )

    if work_space_response is None:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = "please fill all fields")

    return work_space_response

@router.delete('/{user_id}'f'/{work_ep}''/{work_space_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_work_space(
    db: db_dependency,
    user_id: Annotated[int, Path(...)],
    work_space_id: Annotated[int, Path(...)]
):
    work_space_response = work_space_service.soft_delete_work_space(
        db = db,
        user_id = user_id,
        work_space_id = work_space_id
    )

    if work_space_response is None:
        raise HTTPException(status_code = status.HTTP_422_UNPROCESSABLE_ENTITY, detail = 'please fill all fields')

    return {"message": f"delete work space {work_space_response.work_space_name} successfully"}