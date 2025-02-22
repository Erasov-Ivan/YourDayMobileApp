from fastapi import APIRouter
import logging
from backend.config import get_db_connection, configure_logging, encode_jwt_token, decode_jwt_token, DATE_FORMAT

log = logging.getLogger('Users Routes')
configure_logging()

db = get_db_connection()


router = APIRouter(prefix="/users", tags=[])
from .auth_router import router as auth_router
router.include_router(auth_router)
from .pincode_router import router as pincode_router
router.include_router(pincode_router)
from .general_texts_router import router as general_texts_router
router.include_router(general_texts_router)
from .subscription_texts_router import router as subscription_texts_router
router.include_router(subscription_texts_router)
