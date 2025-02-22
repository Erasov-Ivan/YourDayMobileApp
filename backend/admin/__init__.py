from fastapi import APIRouter
import logging
from backend.config import get_db_connection, configure_logging, encode_jwt_token, decode_jwt_token, DATE_FORMAT

log = logging.getLogger('Admin Routes')
configure_logging()

db = get_db_connection()


router = APIRouter(prefix="/admin", tags=[])
from .users_router import router as users_router
router.include_router(users_router)
from .general_texts_router import router as general_texts_router
router.include_router(general_texts_router)
from .subscriptions_router import router as subscriptions_router
router.include_router(subscriptions_router)
from .subscriptions_texts_router import router as subscriptions_texts_router
router.include_router(subscriptions_texts_router)