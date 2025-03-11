from fastapi import APIRouter
import datetime
from schemas import *
from models import *
from . import db, log, DATE_FORMAT, encode_jwt_token, email_sender
import random


router = APIRouter(prefix="/auth", tags=["Users Authentication"])


@router.post("/new", response_model=BaseResponse)
async def auth_new_user(
        email: str,
        name: str,
        bdate: str
):
    try:
        email = email.lower()
        result = await db.get_users_by_email(email=email)
        if len(result) > 0:
            user = result[0]
            code = str(random.randint(10000, 99999))
            await db.update_user_current_code(user_id=user.id, current_code=code)
            await email_sender.send_code(send_to=email, code=code)
            return BaseResponse()
        else:
            bday = datetime.datetime.strptime(bdate, DATE_FORMAT)
            code = str(random.randint(10000, 99999))
            user = User(
                email=email,
                name=name,
                bdate=bday,
                approved=False,
                current_code=code
            )
            await db.new_user(user=user)
            await email_sender.send_code(send_to=email, code=code)
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/enter_code", response_model=BaseResponse)
async def auth_enter_code(
        email: str,
        code: str
):
    try:
        email = email.lower()
        users = await db.get_users_by_email(email=email)
        if len(users) == 0:
            return BaseResponse(error=True, message="User with this email does not exist")
        else:
            user = users[0]
            if user.current_code == code:
                data = f'{user.id}:{user.email}'
                token = await encode_jwt_token(data=data)
                if token is None:
                    raise Exception('Wrong data to generate token')
                await db.approve_user(user_id=user.id, approved=True)
                await db.set_subscription_to_user(
                    subscription=UserHasSubscription(
                        user_id=user.id,
                        subscription='BASIC',
                        expires=datetime.datetime.now() + datetime.timedelta(days=7)
                    )
                )
                await db.update_user_current_code(user_id=user.id, current_code=None)
                return BaseResponse(payload=token)
            else:
                return BaseResponse(error=True, message="Wrong code")

    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/resend_code", response_model=BaseResponse)
async def auth_resend_code(
        email: str,
):
    try:
        email = email.lower()
        users = await db.get_users_by_email(email=email)
        if len(users) == 0:
            return BaseResponse(error=True, message="User with this email does not exist")
        else:
            user = users[0]
            code = str(random.randint(10000, 99999))
            await db.update_user_current_code(user_id=user.id, current_code=code)
            await email_sender.send_code(send_to=email, code=code)
            return BaseResponse()

    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

