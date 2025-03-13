from . import db, decode_jwt_token
import datetime
from models import *
from schemas import *
from .predictions_calculator import calculate_prediction
import logging


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


async def update_subscription(subscription_id: str, user_id: int, months: int):
    user_subscription = await db.get_user_subscription(user_id=user_id, subscription_id=subscription_id)
    if user_subscription is None:
        if months == -1:
            await db.set_subscription_to_user(
                subscription=UserHasSubscription(
                    user_id=user_id,
                    subscription=subscription_id,
                    expires=None
                )
            )
        else:
            await db.set_subscription_to_user(
                subscription=UserHasSubscription(
                    user_id=user_id,
                    subscription=subscription_id,
                    expires=datetime.datetime.now() + datetime.timedelta(days=months * 30)
                )
            )
    else:
        if months == -1:
            await db.update_user_subscription(
                user_id=user_id,
                subscription_id=subscription_id,
                expires=None
            )
        else:
            if user_subscription.expires is not None:
                if user_subscription.expires >= datetime.datetime.now():
                    await db.update_user_subscription(
                        user_id=user_id,
                        subscription_id=subscription_id,
                        expires=user_subscription.expires + datetime.timedelta(days=months * 30)
                    )
                else:
                    await db.update_user_subscription(
                        user_id=user_id,
                        subscription_id=subscription_id,
                        expires=datetime.datetime.now() + datetime.timedelta(days=months * 30)
                    )


async def process_payment(user_email: str, subscription: str, months: int, cost: int):
    if not await db.check_interval(subscription_id=subscription, months=months, cost=cost):
        logging.critical(f'Wrong subscription interval: {subscription}, {months} months, {cost}')
        return

    users = await db.get_users_by_email(email=user_email)
    if len(users) == 0:
        logging.critical(f'User with email {user_email} not found during payment')
        return

    user = users[0]
    if subscription == 'EXTENDED':
        await update_subscription(subscription_id='BASIC', user_id=user.id, months=months)
        await update_subscription(subscription_id='EXTENDED', user_id=user.id, months=months)
    elif subscription == 'BASIC':
        await update_subscription(subscription_id='BASIC', user_id=user.id, months=months)
    else:
        raise Exception(f'No handler for subscription type: {subscription}')

