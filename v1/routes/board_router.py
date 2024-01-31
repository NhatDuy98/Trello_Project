from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from sqlalchemy.orm import Session
from typing import Annotated

from core.database import get_db
from core.config import get_settings
from v1.models import boards, members
from v1.services import board_service, member_service
from v1.schemas import board_schemas, member_schemas

settings = get_settings()
board_ep = settings.END_POINT_BOARD
member_ep = settings.END_POINT_MEMBER

router = APIRouter(
    tags = ["Boards"],
    responses = {404: {"description": "Board not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get(f'/{board_ep}', response_model = board_schemas.BoardResponse, status_code = status.HTTP_200_OK)
def get_all_boards(
    db: db_dependency,
    page: Annotated[int, Query()] = 1,
    limit: Annotated[int, Query] = 5,
    sort_by: Annotated[str, Query()] = None,
    sort_desc: Annotated[bool, Query()] = False,
    search: Annotated[str, Query()] = None
):

    board_sv = board_service.BoardService(db = db, board = boards.Board)

    data_response = board_sv.get_all(
        page = page,
        limit = limit,
        sort_by = sort_by,
        sort_desc = sort_desc,
        search = search
    )

    return data_response

@router.get(f'/{board_ep}''/{id}', response_model = board_schemas.Board, status_code = status.HTTP_200_OK)
def get_board_with_id(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    board = board_service.BoardService(db = db, board = boards.Board)

    board_response = board.get_by_id(id = id)

    if board_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')

    return board_response

@router.post('/{user_id}/{work_space_id}/'f'{board_ep}', response_model = board_schemas.Board, status_code = status.HTTP_201_CREATED)
async def create_board(
    db: db_dependency,
    user_id: Annotated[int, Path(...)],
    work_space_id: Annotated[int, Path(...)],
    board: Annotated[board_schemas.BoardCreate, Body(...)]
):
    board_sv = board_service.BoardService(
        db = db,
        board = boards.Board
    )

    board_response = await board_sv.create_board(user_id = user_id, 
                                           work_space_id = work_space_id, 
                                           board_create = board)
    
    if board_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')

    return board_response

@router.patch(f'/{board_ep}''/{board_id}', response_model = board_schemas.BoardUpdated, status_code = status.HTTP_201_CREATED)
def update_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    board: Annotated[board_schemas.BoardUpdate, Body(...)]
):
    board_sv = board_service.BoardService(db = db, board = boards.Board)

    board_response = board_sv.update_board(id = board_id, board_update = board)

    if board_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'create failed')

    return board_response

@router.delete(f'/{board_ep}''/{id}', status_code = status.HTTP_204_NO_CONTENT)
def soft_delete_board(
    db: db_dependency,
    id: Annotated[int, Path(...)]
):
    board = board_service.BoardService(db = db, board = boards.Board)

    board_response = board.soft_delete(id = id)

    return {'message': f'delete {board_response.board_name} successfully'}

@router.get(f'/{board_ep}''/{board_id}'f'/{member_ep}')
def get_all_members_in_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    search: Annotated[str, Query()] = None
):
    member = member_service.MemberService(db = db, member = members.Member)

    member_responses = member.get_all(board_id = board_id, search = search)

    return member_responses

@router.post(f'/{board_ep}''/{board_id}'f'/{member_ep}', status_code = status.HTTP_201_CREATED)
async def add_member_to_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    user: Annotated[member_schemas.UserAdd, Body(...)]
):

    member = member_service.MemberService(db = db, member = members.Member)

    member_response = await member.add_member(board_id = board_id, user = user)

    return {'message': f'add {user.email} successfull'}

@router.delete(f'/{board_ep}''/{board_id}'f'/{member_ep}''/{member_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_member(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    member_id: Annotated[int, Path(...)]
):
    member = member_service.MemberService(db = db, member = members.Member)

    member_response = member.remove_member(board_id = board_id, member_id = member_id)

    if member_response is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete false')

    return {'message': 'delete successful'}
