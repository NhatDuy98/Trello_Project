from fastapi import APIRouter
from core.config import get_settings
from core.database import engine
from v1.routes.card_router import router as card_router
from v1.routes.label_router import router as label_router
from v1.models import labels, cards, label_cards

labels.Base.metadata.create_all(bind = engine)
cards.Base.metadata.create_all(bind = engine)
label_cards.Base.metadata.create_all(bind = engine)

settings = get_settings()

v1_router = APIRouter(
    prefix = settings.END_POINT_V1
)

v1_router.include_router(label_router)
v1_router.include_router(card_router)