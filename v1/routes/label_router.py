from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import labels, label_cards
from v1.services import label_service
from v1.schemas import label_schemas


labels.Base.metadata.create_all( bind = engine )
label_cards.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Label"],
    responses = {404: {"description": "Label not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/{board_id}/labels', response_model = label_schemas.LabelResponse, status_code = status.HTTP_200_OK)
def get_all_labels(
    db: db_dependency,
    board_id: Annotated[int, Path(...)]
):
    labels = label_service.get_all(db = db, board_id = board_id)
    return labels

@router.get('/labels/{label_id}', response_model = label_schemas.Label, status_code = status.HTTP_200_OK)
def get_label_by_id(
    db: db_dependency,
    label_id: Annotated[int, Path(...)]
):
    label = label_service.get_by_id(db = db, label_id = label_id)

    return label

@router.post('/{board_id}/labels', response_model = label_schemas.Label, status_code = status.HTTP_201_CREATED)
def create_label(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label: Annotated[label_schemas.LabelCreate, Body(...)]
):
    label_response = label_service.create_label(db = db, board_id = board_id, label = label)

    if label_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'create fail')

    return label_response

@router.patch('/{board_id}/labels/{label_id}', response_model = label_schemas.LabelUpdated, status_code = status.HTTP_200_OK)
def update_board(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label_id: Annotated[int, Path(...)],
    label: Annotated[label_schemas.LabelUpdate, Body(...)]
):
    label_response = label_service.update_label(db = db, board_id = board_id, label = label, label_id = label_id)

    if label_response is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = 'update fail')

    return label_response

@router.delete('/{board_id}/labels/{label_id}', status_code = status.HTTP_200_OK)
def delete_label(
    db: db_dependency,
    board_id: Annotated[int, Path(...)],
    label_id: Annotated[int, Path(...)]
):
    label_remove = label_service.delete_label(db = db, board_id = board_id, label_id = label_id)

    if label_remove is False:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = 'delete false')

    return {'message': 'delete successfully'}