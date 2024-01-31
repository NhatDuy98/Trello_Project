from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from core.config import get_settings
from v1.models import labels, label_cards
from v1.services import label_service
from v1.schemas import label_schemas

settings = get_settings()

label_ep = settings.END_POINT_LABEL

router = APIRouter(
    tags = ["Label"],
    responses = {404: {"description": "Label not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/{board_id}'f'/{label_ep}', response_model = label_schemas.LabelResponse, status_code = status.HTTP_200_OK)
def get_all_labels(
    db: db_dependency,
    board_id: Annotated[int, Path(...)]
):
    label_sv = label_service.LabelService(db = db, label = labels.Label)

    label_response = label_sv.get_all(board_id = board_id)
    return label_response

@router.get(f'/{label_ep}''/{label_id}', response_model = label_schemas.Label, status_code = status.HTTP_200_OK)
def get_label_by_id(
    db: db_dependency,
    label_id: Annotated[int, Path(...)]
):
    label_sv = label_service.LabelService(db = db, label = labels.Label)

    label = label_sv.get_by_id(label_id = label_id)

    if label is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'label not found')

    return label

@router.post('/{board_id}'f'/{label_ep}', response_model = label_schemas.Label, status_code = status.HTTP_201_CREATED)
async def create_label(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label: Annotated[label_schemas.LabelCreate, Body(...)]
):
    label_sv = label_service.LabelService(db = db, label = labels.Label)

    label_response = await label_sv.create_label(board_id = board_id, label = label)

    if label_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'create fail')

    return label_response

@router.patch('/{board_id}'f'/{label_ep}''/{label_id}', response_model = label_schemas.LabelUpdated, status_code = status.HTTP_201_CREATED)
async def update_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label_id: Annotated[int, Path(...)],
    label: Annotated[label_schemas.LabelUpdate, Body(...)]
):
    label_sv = label_service.LabelService(db = db, label = labels.Label)

    label_response = await label_sv.update_label(board_id = board_id, label = label, label_id = label_id)

    if label_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'update failed')

    return label_response

@router.delete('/{board_id}'f'/{label_ep}''/{label_id}', status_code = status.HTTP_204_NO_CONTENT)
async def delete_label(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label_id: Annotated[int, Path(...)]
):
    label_sv = label_service.LabelService(db = db, label = labels.Label)

    label_remove = await label_sv.delete_label(board_id = board_id, label_id = label_id)

    if label_remove is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete false')

    return {'message': 'delete successfully'}