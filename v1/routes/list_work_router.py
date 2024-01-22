from fastapi import APIRouter, status, Depends, Path, HTTPException, Body
from core.database import get_db
from core.config import get_settings
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import list_works
from v1.services import list_work_service
from v1.schemas import list_work_schemas

settings = get_settings()

router = APIRouter(
    tags = ["ListWork"],
    responses = {404: {"description": "ListWork not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(f'/{settings.END_POINT_LIST}', response_model = list_work_schemas.ListWorkResponse, status_code = status.HTTP_200_OK)
async def get_all_list_work(
    db: db_dependency
):
    list_service = list_work_service.ListWorkService(db = db, list_work = list_works.ListWork)
    list_work_response = list_service.get_all()
    return list_work_response

@router.post('/{board_id}'f'/{settings.END_POINT_LIST}', response_model = list_work_schemas.ListWork, status_code = status.HTTP_201_CREATED)
async def create_list_work(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_work: Annotated[list_work_schemas.ListWorkCreate, Body(...)]
):
    list_service = list_work_service.ListWorkService(db = db, list_work = list_works.ListWork)

    list_work_response = await list_service.create_list(list_work = list_work, board_id = board_id)

    if list_work_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create fail')

    return list_work_response

@router.put('/{board_id}'f'/{settings.END_POINT_LIST}''/{list_id}', response_model = list_work_schemas.ListWork, status_code = status.HTTP_200_OK)
async def update_list_work(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_id: Annotated[int, Path(...)],
    list_work: Annotated[list_work_schemas.ListWorkUpdate, Body(...)]
):
    list_service = list_work_service.ListWorkService(db = db, list_work = list_works.ListWork)

    list_work_response = await list_service.update_list(board_id = board_id, 
                                                list_id = list_id, 
                                                list_work = list_work)
    
    return list_work_response

@router.delete('/{board_id}'f'/{settings.END_POINT_LIST}''/{list_id}', status_code = status.HTTP_200_OK)
async def soft_delete(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_id: Annotated[int, Path(...)]
):
    list_service = list_work_service.ListWorkService(db = db, list_work = list_works.ListWork)

    list_work_response = await list_service.soft_delete(board_id = board_id, list_id = list_id)

    return {'message': f'delete list {list_work_response.list_work_name} successful'}