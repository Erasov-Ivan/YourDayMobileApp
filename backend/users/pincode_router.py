from fastapi import APIRouter
from schemas import *
from .utils import *
from . import db, log
import random


router = APIRouter(prefix="/pincode", tags=["Users PinCode"])


@router.post("/reset", response_model=BaseResponse)
async def pincode_reset(
        token: str
):
    try:
        user = await get_user_by_token(token=token)
    except Exception as e:
        log.error(f"Invalid token: {token}, {str(e)}")
        return BaseResponse(error=True, message="Invalid token")

    try:
        code = str(random.randint(10000, 99999))
        await db.update_user_current_code(user_id=user.id, current_code=code)
        return BaseResponse(payload=code)

    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/enter_code", response_model=BaseResponse)
async def pincode_enter_code(
        token: str,
        code: str
):
    try:
        user = await get_user_by_token(token=token)
    except Exception as e:
        log.error(f"Invalid token: {token}, {str(e)}")
        return BaseResponse(error=True, message="Invalid token")

    try:
        if user.current_code != code:
            return BaseResponse(error=True, message="Wrong code")
        else:
            await db.update_user_current_code(user_id=user.id, current_code=None)
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/resend_code", response_model=BaseResponse)
async def pincode_resend_code(
        token: str,
):
    try:
        user = await get_user_by_token(token=token)
    except Exception as e:
        log.error(f"Invalid token: {token}, {str(e)}")
        return BaseResponse(error=True, message="Invalid token")

    try:
        code = str(random.randint(10000, 99999))
        await db.update_user_current_code(user_id=user.id, current_code=code)
        return BaseResponse(payload=code)

    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

