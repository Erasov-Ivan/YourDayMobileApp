from fastapi import APIRouter
from schemas import *
from models import *
from .utils import *
import datetime
from . import db, log, DATE_FORMAT


router = APIRouter(prefix="/subscription_texts", tags=["Users Subscription Texts"])


@router.get("/get_predictions", response_model=PredictionsListResponse)
async def get_predictions(
        language: str,
        bdate: str,
        start_date: str,
        days: int,
        token: str
):
    try:
        birthdate = datetime.datetime.strptime(bdate, DATE_FORMAT)
        start_date = datetime.datetime.strptime(start_date, DATE_FORMAT)
        user = await get_user_by_token(token=token)
        user_subscriptions = await db.get_user_subscriptions(user_id=user.id)
        if len(user_subscriptions) == 0:
            return BaseResponse()
        else:
            predictions = []
            for day in range(days):
                subscriptions: dict[str, dict[str, PredictionFieldModel]] = {}
                for subscription in user_subscriptions:
                    if subscription.expires is None or subscription.expires >= datetime.datetime.now():
                        subscriptions[subscription.subscription] = await generate_prediction(
                            date=start_date + datetime.timedelta(days=day),
                            birthdate=birthdate,
                            language=language,
                            subscription_id=subscription.subscription
                        )
                predictions.append(
                    PredictionModel(
                        date=(datetime.date.today() + datetime.timedelta(days=day)).strftime(DATE_FORMAT),
                        subscriptions=subscriptions
                    )
                )
            return PredictionsListResponse(
                payload=PredictionsListModel(
                    predictions=predictions
                )
            )

    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

