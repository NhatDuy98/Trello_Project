from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.repository import label_repo, label_card_repo
from v1.schemas import label_schemas
from v1.services import label_card_service
from v1.models.labels import Label
from v1.models.boards import Board

def get_all(
    db: Session,
    board_id: int
) -> label_schemas.LabelResponse:
    db_board = db.query(Board).filter(Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')

    db_label = label_repo.get_all(db = db, board_id = board_id)

    data_response = label_schemas.LabelResponse(data = [label.to_dto() for label in db_label])

    return data_response

def get_by_id(
    db: Session,
    label_id: int
):
    db_board = label_repo.get_by_id(db = db, id = label_id)

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')

    return db_board.to_dto()

def create_label(
    db: Session,
    board_id: int,
    label: label_schemas.LabelCreate
):
    if not label.dict():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_board = db.query(Board).filter(Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    labels_check = label_repo.get_all(db = db, board_id = board_id)

    for i in labels_check:
        if i.color == label.color and i.label_name == label.label_name:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')

    db_label = Label(**label.dict(), board_id = board_id)

    db.add(db_label)
    db.commit()
    db.refresh(db_label)

    return db_label.to_dto()

def update_label(
    db: Session,
    board_id: int,
    label_id: int,
    label: label_schemas.LabelUpdate
):
    if not label.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_board = db.query(Board).filter(Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    if db_board.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_label = label_repo.get_by_id(db = db, id = label_id)

    if db_label is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')
    
    labels_check = label_repo.get_all(db = db, board_id = board_id)

    for i in labels_check:
        if i.color == label.color and i.label_name == label.label_name:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')
    
    for field in label.dict(exclude_unset = True):
        setattr(db_label, field, getattr(label, field))

    db.add(db_label)
    db.commit()
    db.refresh(db_label)

    return db_label.to_dto()

def delete_label(
    db: Session,
    board_id: int,
    label_id: int
):
    db_board = db.query(Board).filter(Board.id == board_id).first()

    if db_board is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'board not found')
    
    db_label_card = label_card_repo.get_all_with_label(db = db, label_id = label_id)

    for i in db_label_card:
        label_card_service.remove_label(db = db, card_id = i.card_id, label_card_id = label_id)
    
    db_label = label_repo.get_by_id(db = db, id = label_id)

    db.delete(db_label)
    db.commit()

    label_check = label_repo.get_by_id(db = db, id = label_id)

    if label_check:
        return False

    return True