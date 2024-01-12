from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import boards


boards.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["Boards"],
    responses = {404: {"description": "Board not found"}}
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/boards')
def get_all_list_work(
    db: db_dependency,

):
    return