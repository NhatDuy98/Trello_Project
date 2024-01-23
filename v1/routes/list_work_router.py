from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import list_works
from v1.services import list_work_service
from v1.schemas import list_work_schemas


list_works.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["ListWork"],
    responses = {404: {"description": "ListWork not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/lists', status_code = status.HTTP_200_OK)
def get_all_list_work(
    db: db_dependency
):
    list_work_response = list_work_service.find_all(db)
    return list_work_response

@router.post('/{board_id}/lists', response_model = list_work_schemas.ListWork, status_code = status.HTTP_201_CREATED)
def create_list_work(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_work: Annotated[list_work_schemas.ListWorkCreate, Body(...)]
):
    list_work_response = list_work_service.create_list_work(db = db, list_work = list_work, board_id = board_id)

    if list_work_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create fail')

    return list_work_response

@router.put('/{board_id}/lists/{list_id}', response_model = list_work_schemas.ListWork, status_code = status.HTTP_200_OK)
def update_list_work(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_id: Annotated[int, Path(...)],
    list_work: Annotated[list_work_schemas.ListWorkUpdate, Body(...)]
):
    list_work_response = list_work_service.update_list(db = db, 
                                                       board_id = board_id, 
                                                       list_id = list_id, 
                                                       list_work = list_work)
    
    return list_work_response

@router.delete('/{board_id}/lists/{list_id}', status_code = status.HTTP_200_OK)
def soft_delete(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_id: Annotated[int, Path(...)]
):
    list_work_response = list_work_service.soft_delete(db = db, board_id = board_id, list_id = list_id)

    return {'message': f'delete successful'}