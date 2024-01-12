from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from v1.repository import label_card_repo, label_repo, card_repo
from v1.schemas import label_card_schemas
from v1.models.label_cards import LabelCard
from v1.models.list_works import ListWork

def add_label_to_card(
    db: Session,
    board_id: int,
    list_work_id: int,
    card_id: int,
    label: label_card_schemas.LabelAdd
):
    db_label = label_repo.get_by_id(db = db, id = label.id)

    if db_label is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')
    
    if db_label.board_id != board_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not add label in another board')
    
    db_list_work = db.query(ListWork).filter(ListWork.id == list_work_id).first()

    if db_list_work is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'list not found')

    if db_list_work.board_id != board_id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = 'not add label in another board')

    label_check = label_card_repo.get_all(db = db, card_id = card_id)

    for i in label_check:
        if i.label_id == label.id:
            raise HTTPException(status_code = status.HTTP_409_CONFLICT, detail = 'duplicate')

    db_label_card = LabelCard(card_id = card_id, label_id = label.id)

    db.add(db_label_card)
    db.commit()
    db.refresh(db_label_card)

    return db_label_card

def remove_label(
    db: Session,
    card_id: int,
    label_card_id: int
):
    db_card = card_repo.get_by_id(db = db, id = card_id)

    if db_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'card not found')

    db_label_card = label_card_repo.get_by_id(db = db, id = label_card_id)

    if db_label_card is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'not found')
    
    db.delete(db_label_card)
    db.commit()

    return