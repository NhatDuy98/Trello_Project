from fastapi import APIRouter, status, Depends
from core.database import get_db
from sqlalchemy.orm import Session

