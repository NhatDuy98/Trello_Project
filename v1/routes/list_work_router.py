from fastapi import APIRouter, status, Depends, Query, Path, HTTPException, Body
from core.database import get_db, engine
from sqlalchemy.orm import Session
from typing import Annotated
from v1.models import list_works


list_works.Base.metadata.create_all( bind = engine )

router = APIRouter(
    prefix = "/api/v1",
    tags = ["ListWork"],
    responses = {404: {"description": "ListWork not found"}}
)