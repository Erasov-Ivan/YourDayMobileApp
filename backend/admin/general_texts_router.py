from fastapi import APIRouter
from backend.schemas import *
from backend.models import *
from . import db, log


router = APIRouter(prefix="/general_texts", tags=["Admin General Texts"])


@router.post("/new_field", response_model=BaseResponse)
async def new_field(
    field_id: str,
    description: str = ''
):
    try:
        if await db.is_filed_exists(field_id=field_id):
            return BaseResponse(error=True, message="Field already exists")
        else:
            await db.new_field(
                field=TextField(
                    id=field_id,
                    description=description
                )
            )
            return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/new_text", response_model=BaseResponse)
async def new_text(
    field_id: str,
    language: str,
    text: str
):
    try:
        if not await db.is_filed_exists(field_id=field_id):
            return BaseResponse(error=True, message="Field do not exists")
        else:
            if await db.is_text_exists(field_id=field_id, language=language):
                return BaseResponse(error=True, message="Text with such language already exists")
            else:
                await db.new_text(
                    text=GeneralTexts(
                        field_id=field_id,
                        language=language,
                        text=text
                    )
                )
                return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.post("/update_text", response_model=BaseResponse)
async def update_text(
    field_id: str,
    language: str,
    text: str,
    create_if_not_exists: bool = False
):
    try:
        if not await db.is_filed_exists(field_id=field_id):
            return BaseResponse(error=True, message="Field do not exists")
        else:
            if not await db.is_text_exists(field_id=field_id, language=language):
                if not create_if_not_exists:
                    return BaseResponse(error=True, message="Text with such language do not exists")
                else:
                    await db.new_text(
                        text=GeneralTexts(
                            field_id=field_id,
                            language=language,
                            text=text
                        )
                    )
                    return BaseResponse()
            else:
                await db.update_general_text(
                    field_id=field_id,
                    language=language,
                    text=text
                )
                return BaseResponse()
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))


@router.get("/list", response_model=FieldsListResponse)
async def get_fields_list(
        limit: int = 10,
        offset: int = 0,
        language: str = None,
):
    try:
        fields = await db.get_general_fields(limit=limit, offset=offset)
        total_count = await db.count_general_fields()
        return FieldsListResponse(
            payload=FieldsListModel(
                total_count=total_count,
                fields=[
                    FieldModel(
                        id=field.id,
                        description=field.description,
                        texts=[
                            TextModel(
                                language=text.language,
                                text=text.text
                            ) for text in await db.get_general_texts_by_filed_id(field_id=field.id, language=language)
                        ]
                    ) for field in fields
                ]
            )
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

