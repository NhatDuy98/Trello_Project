from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.models import list_works, boards
from v1.repository import list_work_repo
from v1.schemas import list_work_schemas

def find_all(
    db: Session
) -> list_work_schemas.ListWorkResponse:
    list_works = list_work_repo.get_all(db)

    data_response = list_work_schemas.ListWorkResponse(data = [list.to_dto() for list in list_works])

    return data_response


def create_list_work(
    db: Session,
    list_work: list_work_schemas.ListWorkCreate,
    board_id: int
):
    db_board = db.query(boards.Board).filter(boards.Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

    db_list = list_works.ListWork(**list_work.dict(), board_id = board_id)

    db.add(db_list)
    db.commit()
    db.refresh(db_list)

    return db_list.to_dto()

def update_list(
    db: Session,
    board_id: int,
    list_id: int,
    list_work: list_work_schemas.ListWorkUpdate
):
    if not list_work.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'bad request')

    db_board = db.query(boards.Board).filter(boards.Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_list = list_work_repo.get_by_id(db = db, id = list_id)

    if db_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
    if db_list.is_delete:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    for field in list_work.dict(exclude_unset = True):
        setattr(db_list, field, getattr(list_work, field))

    db.add(db_list)
    db.commit()
    db.refresh(db_list)

    return db_list.to_dto()


def soft_delete(
    db: Session,
    board_id: int,
    list_id: int
):
    db_board = db.query(boards.Board).filter(boards.Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_list = list_work_repo.get_by_id(db = db, id = list_id)

    if db_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
    if db_list.is_delete:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    db_list.is_delete = True
    db_list.deleted_at = datetime.now()

    db.commit()

    return db_list.to_dto()