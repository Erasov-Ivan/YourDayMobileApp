from fastapi import APIRouter
from schemas import *
from . import db, log, DATE_FORMAT
from .utils import get_user_by_token
import datetime

router = APIRouter(prefix="/subscriptions", tags=["Users Subscriptions"])


@router.get("/list", response_model=UserSubscriptionsResponse)
async def get_user_subscriptions(
        token: str
):
    try:
        user = await get_user_by_token(token=token)
        user_subscriptions = await db.get_user_subscriptions(user_id=user.id)
        result = UserSubscriptionsModel()
        for user_subscription in user_subscriptions:
            if user_subscription.expires is None or user_subscription.expires >= datetime.datetime.now():
                if user_subscription.subscription == 'BASIC':
                    if user_subscription.expires is not None:
                        result.basic = user_subscription.expires.strftime(DATE_FORMAT)
                    else:
                        result.basic = 'ENDLESS'
                elif user_subscription.subscription == 'EXTENDED':
                    if user_subscription.expires is not None:
                        result.extended = user_subscription.expires.strftime(DATE_FORMAT)
                    else:
                        result.extended = 'ENDLESS'
        return UserSubscriptionsResponse(
            payload=result
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.get("/options", response_model=SubscriptionOptionsResponse)
async def get_subscription_options():
    try:
        options = await db.get_subscription_intervals()
        return SubscriptionOptionsResponse(
            payload=SubscriptionOptionsListModel(
                options=[
                    SubscriptionOptionModel(
                        subscription_id=option.subscription_id,
                        months=option.months,
                        cost=option.cost
                    ) for option in options
                ]
            )
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))