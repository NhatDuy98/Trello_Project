from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from v1.repository import card_repo
from v1.schemas import card_schemas
from v1.models.cards import Card
from v1.models.boards import Board
from v1.models.list_works import ListWork

def get_all(
    db: Session
) -> card_schemas.CardResponse:
    cards = card_repo.get_all(db)

    card_response = card_schemas.CardResponse(data = [card.to_dto() for card in cards])

    return card_response

def create_card(
    db: Session,
    list_work_id: int,
    card: card_schemas.CardCreate
):
    if not card.dict():
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_list = db.query(ListWork).filter(ListWork.id == list_work_id).first()

    if db_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
    if db_list.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'system error')
    
    db_card = Card(**card.dict(), list_work_id = list_work_id)

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    return db_card.to_dto()


def update_card(
    db: Session,
    list_id: int,
    card_id: int,
    card: card_schemas.CardUpdate
):
    if not card.dict(exclude_unset = True):
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')

    db_list = db.query(ListWork).filter(ListWork.id == list_id).first()

    if db_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
    if db_list.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_card = card_repo.get_by_id(db = db, id = card_id)

    if db_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
    if db_card.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    if db_card.list_work_id != list_id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    for field in card.dict(exclude_unset = True):
        setattr(db_card, field, getattr(card, field))

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    return db_card.to_dto()

def update_action_move_card(
    db: Session,
    card_id: int,
    list: card_schemas.CardUpdateMove
):

    db_card = card_repo.get_by_id(db = db, id = card_id)

    if db_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
    if db_card.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_card.list_work_id = list.list_work_id

    db.add(db_card)
    db.commit()
    db.refresh(db_card)

    if db_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'move fail')

    return db_card

def soft_delete(
    db: Session,
    list_id: int,
    card_id: int
):
    db_list = db.query(ListWork).filter(ListWork.id == list_id).first()

    if db_list is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')
    
    if db_list.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    db_card = card_repo.get_by_id(db = db, id = card_id)

    if db_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')
    
    if db_card.is_delete:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not allow')
    
    if db_card.list_work_id != list_id:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'system error')
    
    db_card.is_delete = True
    db_card.deleted_at = datetime.now()

    db.commit()

    if db_card.is_delete is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete fail')

    return db_card