from fastapi import APIRouter
from core.config import get_settings
from core.database import engine
from v1.routes.list_work_router import router as list_work_router
from v1.models import list_works

list_works.Base.metadata.create_all(bind = engine)

settings = get_settings()

v1_router = APIRouter(
    prefix = settings.END_POINT_V1
)

v1_router.include_router(list_work_router)