from fastapi import APIRouter
from schemas import *
from models import *
from . import db, log


router = APIRouter(prefix="/subscriptions", tags=["Admin Subscriptions"])


@router.post("/new", response_model=BaseResponse)
async def new_subscription(
        id: str,
        description: str
):
    try:
        if await db.is_subscription_exists(subscription_id=id):
            return BaseResponse(error=True, message="Subscription with such id already exists")
        else:
            await db.new_subscription(
                subscription=Subscription(
                    id=id,
                    description=description
                )
            )
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.get("/list", response_model=SubscriptionsListResponse)
async def subscriptions_list():
    try:
        subscriptions = await db.get_subscriptions()
        return SubscriptionsListResponse(
            payload=SubscriptionListModel(
                subscriptions=[
                    SubscriptionModel(
                        id=subscription.id,
                        description=subscription.description
                    ) for subscription in subscriptions
                ]
            )
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

