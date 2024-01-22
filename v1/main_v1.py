from fastapi import APIRouter
from core.config import get_settings
from core.database import engine
from v1.routes.board_router import router as board_router
from v1.models import boards, members

boards.Base.metadata.create_all(bind = engine)
members.Base.metadata.create_all(bind = engine)

settings = get_settings()

v1_router = APIRouter(
    prefix = settings.END_POINT_V1
)

v1_router.include_router(board_router)