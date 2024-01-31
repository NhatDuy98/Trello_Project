from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from core.config import get_settings
from v1.models import cards, label_cards
from v1.services import card_service, label_card_service
from v1.schemas import card_schemas, label_card_schemas

settings = get_settings()

card_ep = settings.END_POINT_CARD
card_label_ep = settings.END_POINT_LABEL_CARD

router = APIRouter(
    tags = ["Card"],
    responses = {404: {"description": "Card not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/{list_work_id}'f'/{card_ep}', response_model = card_schemas.CardResponse, status_code = status.HTTP_200_OK)
def get_all_cards(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)]
):
    card_sv = card_service.CardService(db = db, card = cards.Card)

    responses = card_sv.get_all(list_work_id = list_work_id)
    return responses

@router.post('/{list_work_id}'f'/{card_ep}', response_model = card_schemas.Card, status_code = status.HTTP_201_CREATED)
async def create_card(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card: Annotated[card_schemas.CardCreate, Body(...)]
):
    card_sv = card_service.CardService(db = db, card = cards.Card)

    card_response = await card_sv.create_card(list_work_id = list_work_id, card = card)

    if card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'create fail')

    return card_response

@router.patch('/{list_work_id}'f'/{card_ep}''/{card_id}', response_model = card_schemas.CardUpdated, status_code = status.HTTP_201_CREATED)
async def update_card(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)],
    card: Annotated[card_schemas.CardUpdate, Body(...)]
):
    card_sv = card_service.CardService(db = db, card = cards.Card)

    card_response = await card_sv.update_card(list_id = list_work_id, card_id = card_id, card = card)

    if card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'update fail')

    return card_response

@router.delete('/{list_work_id}'f'/{card_ep}''/{card_id}', status_code = status.HTTP_204_NO_CONTENT)
async def soft_delete(
    db: db_dependency,
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)]
):
    card_sv = card_service.CardService(db = db, card = cards.Card)

    card_response = await card_sv.soft_delete(list_id = list_work_id, card_id = card_id)

    return {'message': f'delete {card_response.card_name} successful'}

@router.patch(f'/{card_ep}''/{card_id}', status_code = status.HTTP_201_CREATED)
async def update_action_move_card(
    db: db_dependency,
    card_id: Annotated[int, Path(...)],
    list_work: Annotated[card_schemas.CardUpdateMove, Body(...)]
):
    card_sv = card_service.CardService(db = db, card = cards.Card)

    card_response = await card_sv.update_action_move_card(card_id = card_id, list = list_work)

    if card_response is None:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'update failed')

    return {'message': f'move card {card_response.card_name} successful'}

@router.post('/{board_id}/{list_work_id}'f'/{card_ep}''/{card_id}', status_code = status.HTTP_201_CREATED)
async def add_label_to_card(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    list_work_id: Annotated[int, Path(...)],
    card_id: Annotated[int, Path(...)],
    label: Annotated[label_card_schemas.LabelAdd, Body(...)]
):
    label_card_sv = label_card_service.LabelCardService(db = db, label_card = label_cards.LabelCard)

    label_card_response = await label_card_sv.add_label_to_card(board_id = board_id, 
                                                        list_work_id = list_work_id,
                                                        card_id = card_id, 
                                                        label = label)

    if label_card_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'add failed')

    return {'message': 'add label successful'}

@router.delete(f'/{card_ep}''/{card_id}'f'/{card_label_ep}''/{card_label_id}', status_code = status.HTTP_204_NO_CONTENT)
async def remove_label_from_card(
    db: db_dependency,
    card_id: Annotated[int, Path(...)],
    card_label_id: Annotated[int, Path(...)]
):
    label_card_sv = label_card_service.LabelCardService(db = db, label_card = label_cards.LabelCard)

    card_remove = await label_card_sv.remove_label(card_id = card_id, label_card_id = card_label_id)

    if card_remove is True:
        return {'message': 'remove successful'}