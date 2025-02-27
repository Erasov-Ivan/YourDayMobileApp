from fastapi import APIRouter, Body
from schemas import *
from models import *
from . import db, log


router = APIRouter(prefix="/subscription_texts", tags=["Admin Subscription Texts"])


@router.post("/new_text", response_model=BaseResponse)
async def new_text(
    subscription_id: str,
    language: str,
    field_id: str,
    number: int,
    text: str = Body(..., media_type='text/plain')
):
    try:
        if await db.is_subscription_text_exists(
            subscription_id=subscription_id,
            language=language,
            field_id=field_id,
            number=number
        ):
            return BaseResponse(error=True, message="This text already exists")
        else:
            await db.new_subscription_text(
                text=SubscriptionTexts(
                    field=field_id,
                    language=language,
                    subscription_id=subscription_id,
                    number=number,
                    text=text
                )
            )
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/update_text", response_model=BaseResponse)
async def update_text(
    subscription_id: str,
    language: str,
    field_id: str,
    number: int,
    text: str = Body(..., media_type='text/plain'),
    create_if_not_exists: bool = False
):
    try:
        if not await db.is_subscription_text_exists(
                subscription_id=subscription_id,
                language=language,
                field_id=field_id,
                number=number
        ):
            if not create_if_not_exists:
                return BaseResponse(error=True, message="This text do not exists")
            else:
                await db.new_subscription_text(
                    text=SubscriptionTexts(
                        field=field_id,
                        language=language,
                        subscription_id=subscription_id,
                        number=number,
                        text=text
                    )
                )
                return BaseResponse()
        else:
            await db.update_subscription_text(
                field_id=field_id,
                language=language,
                subscription_id=subscription_id,
                number=number,
                text=text
            )
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.get("/list", response_model=SubscriptionTextsResponse)
async def get_texts_list(
        subscription_id: str = None,
        language: str = None
):
    try:
        texts = await db.get_subscription_texts_list(subscription_id=subscription_id, language=language)
        subscriptions: list[SubscriptionLanguagesModel] = []
        for text in texts:
            found_subscription = False
            for subscription in subscriptions:
                if subscription.subscription_id == text.subscription_id:
                    found_subscription = True
                    found_language = False
                    for language in subscription.languages:
                        if language.language == text.language:
                            found_language = True
                            found_field = False
                            for field in language.fields:
                                if field.field_id == text.field:
                                    found_field = True
                                    field.texts.append(
                                        SubscriptionTextModel(
                                            number=text.number,
                                            text=text.text
                                        )
                                    )
                                    break
                            if not found_field:
                                language.fields.append(
                                    SubscriptionFieldModel(
                                        field_id=text.field,
                                        texts=[
                                            SubscriptionTextModel(
                                                number=text.number,
                                                text=text.text
                                            )
                                        ]
                                    )
                                )
                            break
                    if not found_language:
                        subscription.languages.append(
                            LanguageTextsListModel(
                                language=text.language,
                                fields=[
                                    SubscriptionFieldModel(
                                        field_id=text.field,
                                        texts=[
                                            SubscriptionTextModel(
                                                number=text.number,
                                                text=text.text
                                            )
                                        ]
                                    )
                                ]
                            )
                        )
                    break
            if not found_subscription:
                subscriptions.append(
                    SubscriptionLanguagesModel(
                        subscription_id=text.subscription_id,
                        languages=[
                            LanguageTextsListModel(
                                language=text.language,
                                fields=[
                                    SubscriptionFieldModel(
                                        field_id=text.field,
                                        texts=[
                                            SubscriptionTextModel(
                                                number=text.number,
                                                text=text.text
                                            )
                                        ]
                                    )
                                ]
                            )
                        ]
                    )
                )
        return SubscriptionTextsResponse(
            payload=subscriptions
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

