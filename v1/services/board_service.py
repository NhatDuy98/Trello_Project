from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.repository import board_repo, member_repo
from v1.schemas import board_schemas
from v1.models import boards, members
from v1.services import user_service, work_space_service

def get_all(
    db: Session,
    page: int = 1,
    limit: int = 5,
    sort_by: str = None,
    sort_desc: bool = False,
    search: str = None
) -> board_schemas.BoardResponse:
    boards = board_repo.get_all(
        db = db,
        page = page,
        limit = limit,
        sort_by = sort_by,
        sort_desc = sort_desc,
        search = search
    )

    total = board_repo.count_all(db)

    pagination = board_schemas.PaginationModel(page = page, limit = limit, totalRows = total)

    return board_schemas.BoardResponse(data = [board.to_dto() for board in boards], pagination = pagination)

def get_by_id(
    db: Session,
    id: int
):
    board = board_repo.get_by_id(db, id)

    if board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')

    return board.to_dto()

async def create_board(
    db: Session,
    user_id: int,
    work_space_id: int,
    board: board_schemas.BoardCreate
):
    if board.dict(exclude_unset = True) is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_user = user_service.find_user_by_id(db, user_id)

    if db_user is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'user not found')
    
    if db_user.is_active is False:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

    db_work_space = work_space_service.get_work_space_by_id(db, work_space_id)

    if db_work_space is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'work space not found')
    
    if db_work_space.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_board = boards.Board(**board.dict(), work_space_id = work_space_id)

    board_save = db_board

    db.add(board_save)
    db.commit()
    db.refresh(board_save)

    try:
        if db_board:
            db_member = members.Member(user_id = user_id, board_id = db_board.id, role = 'HOST')
            await member_repo.add_member(db, db_member)
    except HTTPException:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'fail to add member')

    return db_board.to_dto()

def update_board(
    db: Session,
    board_id: int,
    board: board_schemas.BoardUpdate
):
    if not board.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_board = board_repo.get_by_id(db, board_id)

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'can not update board deleted')
    
    for field in board.dict(exclude_unset = True):
        setattr(db_board, field, getattr(board, field))

    db.add(db_board)
    db.commit()
    db.refresh(db_board)

    return db_board.to_dto()

def soft_delete_board(
    db: Session,
    id: int
) -> boards.Board:
    db_board = board_repo.get_by_id(db, id)

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    db_board.is_delete = True
    db_board.deleted_at = datetime.now()

    db.commit()

    return db_board