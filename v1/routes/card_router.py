from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import cards
from v1.services import card_service, label_card_service
from v1.schemas import card_schemas, label_card_schemas

cards.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Card"],
    responses = {404: {"description": "Card not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/cards', response_model = card_schemas.CardResponse, status_code = status.HTTP_200_OK)
def get_all_cards(
    db: db_dependency
):
    cards = card_service.get_all(db = db)
    return cards

@router.post('/{list_work_id}/cards', response_model = card_schemas.Card, status_code = status.HTTP_201_CREATED)
def create_card(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card: Annotated[card_schemas.CardCreate, Body(...)]
):
    card_response = card_service.create_card(db = db, list_work_id = list_work_id, card = card)

    if card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'create fail')

    return card_response

@router.patch('/{list_work_id}/cards/{card_id}', response_model = card_schemas.CardUpdated, status_code = status.HTTP_200_OK)
def update_card(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)],
    card: Annotated[card_schemas.CardUpdate, Body(...)]
):
    card_response = card_service.update_card(db = db, list_id = list_work_id, card_id = card_id, card = card)

    if card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'update fail')

    return card_response

@router.delete('/{list_work_id}/cards/{card_id}', status_code = status.HTTP_200_OK)
def soft_delete(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)]
):
    card_response = card_service.soft_delete(db = db, list_id = list_work_id, card_id = card_id)

    return {'message': f'delete {card_response.card_name} successful'}

@router.patch('/cards/{card_id}', status_code = status.HTTP_200_OK)
def update_action_move_card(
    db: db_dependency,
    card_id: Annotated[int, Path(...)],
    list_work: Annotated[card_schemas.CardUpdateMove, Body(...)]
):
    card_response = card_service.update_action_move_card(db = db, card_id = card_id, list = list_work)

    return {'message': f'move card successful'}

@router.post('/{board_id}/{list_work_id}/cards/{card_id}', status_code = status.HTTP_201_CREATED)
def add_label_to_card(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)],
    label: Annotated[label_card_schemas.LabelAdd, Body(...)]
):
    label_card_response = label_card_service.add_label_to_card(db = db, 
                                                               board_id = board_id, 
                                                               list_work_id = list_work_id,
                                                               card_id = card_id, 
                                                               label = label)

    if label_card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'add fail')

    return {'message': 'add label successful'}

@router.delete('/cards/{card_id}/card_labels/{card_label_id}', status_code = status.HTTP_200_OK)
def remove_label_from_card(
    db: db_dependency,
    card_id: Annotated[int, Path(...)],
    card_label_id: Annotated[int, Path(...)]
):
    card_remove = label_card_service.remove_label(db = db, card_id = card_id, label_card_id = card_label_id)

    return {'message': 'delete successfully'}