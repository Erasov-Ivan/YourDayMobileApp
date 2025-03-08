from . import db, decode_jwt_token
import datetime
from models import *
from schemas import *
from .predictions_calculator import calculate_prediction


async def get_user_by_token(token: str) -> User:
    data = await decode_jwt_token(token=token)
    user_id, email = data.split(':')
    user_id = int(user_id)
    users = await db.get_users_from_token(user_id=user_id, email=email)
    if len(users) == 0:
        raise Exception('No such user')
    else:
        user = users[0]
        return user


async def generate_prediction(
        subscription_id: str, language: str, date: datetime.date, birthdate: datetime.date
) -> dict[str, PredictionFieldModel]:
    a, b, k = await calculate_prediction(
        birthdate=birthdate,
        date=date
    )
    a_text = await db.get_subscription_text(
        subscription_id=subscription_id,
        language=language,
        field_id='FIELD_A',
        number=a
    )
    b_text = await db.get_subscription_text(
        subscription_id=subscription_id,
        language=language,
        field_id='FIELD_B',
        number=b
    )
    k_text = await db.get_subscription_text(
        subscription_id=subscription_id,
        language=language,
        field_id='UNDER_HEART',
        number=k
    )
    colors = await db.get_colors()
    return {
        'FIELD_A': PredictionFieldModel(
            num=a,
            color=colors.get(a),
            text=a_text.text if a_text else None
        ),
        'FIELD_B': PredictionFieldModel(
            num=b,
            color=colors.get(b),
            text=b_text.text if b_text else None
        ),
        'UNDER_HEART': PredictionFieldModel(
            num=k,
            color=colors.get(k),
            text=k_text.text if k_text else None
        )
    }


