from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import boards, members
from v1.services import board_service, member_service
from v1.schemas import board_schemas, member_schemas

boards.Base.metadata.create_all( bind = engine )
members.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Boards"],
    responses = {404: {"description": "Board not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/boards', response_model = board_schemas.BoardResponse, status_code = status.HTTP_200_OK)
def get_all_boards(
    db: db_dependency,
    page: Annotated[int, Query()] = 1,
    limit: Annotated[int, Query] = 5,
    sort_by: Annotated[str, Query()] = None,
    sort_desc: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None
):
    data = board_service.get_all(
        db = db,
        page = page,
        limit = limit,
        sort_by = sort_by,
        sort_desc = sort_desc,
        search = search
    )
    return data

@router.get('/boards/{id}', response_model = board_schemas.Board, status_code = status.HTTP_200_OK)
def get_board_with_id(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    board = board_service.get_by_id(db, id)
    return board

@router.post('/{user_id}/{work_space_id}/boards', response_model = board_schemas.Board, status_code = status.HTTP_201_CREATED)
async def create_board(
    db: db_dependency,
    user_id: Annotated[int, Path(...)],
    work_space_id: Annotated[int, Path(...)],
    board: Annotated[board_schemas.BoardCreate, Body(...)]
):
    board_response = await board_service.create_board(
        db = db,
        user_id = user_id,
        work_space_id = work_space_id,
        board = board
    )

    return board_response

@router.patch('/boards/{board_id}', response_model = board_schemas.BoardUpdated, status_code = status.HTTP_200_OK)
def update_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    board: Annotated[board_schemas.BoardUpdate, Body(...)]
):
    board_response = board_service.update_board(db, board_id, board)

    return board_response

@router.delete('/boards/{id}', status_code = status.HTTP_200_OK)
def soft_delete_board(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    board = board_service.soft_delete_board(db, id)
    return {'message': f'delete {board.board_name} successfully'}

@router.get('/boards/{board_id}/members')
def get_all_members_in_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    search: Annotated[str, Query()] = None
):
    members = member_service.get_all(db, board_id, search)
    return members

@router.post('/boards/{board_id}/members', status_code = status.HTTP_200_OK)
def add_member_to_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    user: Annotated[member_schemas.UserAdd, Body(...)]
):
    member = member_service.add_member(db, board_id, user)

    if member is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'fail')

    return {'message': f'add {user.email} successfull'}

@router.delete('/boards/{board_id}/members/{member_id}', status_code = status.HTTP_200_OK)
def delete_member(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    member_id: Annotated[int, Path(...)]
):
    member = member_service.remove_member(db = db, board_id = board_id, member_id = member_id)

    if member is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete false')

    return {'message': 'delete successful'}