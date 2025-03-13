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
            if user_subscription.expires >= datetime.datetime.now():
                if user_subscription.subscription == 'BASIC':
                    result.basic = user_subscription.expires.strptime(DATE_FORMAT)
                elif user_subscription.subscription == 'EXTENDED':
                    result.extended = user_subscription.expires.strptime(DATE_FORMAT)
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