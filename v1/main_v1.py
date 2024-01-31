from fastapi import APIRouter
from core.config import get_settings
from core.database import engine
from v1.routes.home_router import router as home_router
from v1.routes.user_router import router as user_router
from v1.routes.work_space_router import router as work_space_router
from v1.routes.board_router import router as board_router
from v1.routes.list_work_router import router as list_work_router
from v1.routes.card_router import router as card_router
from v1.routes.label_router import router as label_router
from v1.models import boards, members, labels, cards, label_cards, list_works, users, work_spaces

users.Base.metadata.create_all(bind = engine)
work_spaces.Base.metadata.create_all(bind = engine)
boards.Base.metadata.create_all(bind = engine)
members.Base.metadata.create_all(bind = engine)
list_works.Base.metadata.create_all(bind = engine)
labels.Base.metadata.create_all(bind = engine)
cards.Base.metadata.create_all(bind = engine)
label_cards.Base.metadata.create_all(bind = engine)

settings = get_settings()

v1_router = APIRouter(
    prefix = settings.END_POINT_V1
)

v1_router.include_router(home_router)
v1_router.include_router(user_router)
v1_router.include_router(work_space_router)
v1_router.include_router(board_router)
v1_router.include_router(list_work_router)
v1_router.include_router(label_router)
v1_router.include_router(card_router)
