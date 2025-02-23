from fastapi import APIRouter
from schemas import *
from models import *
from . import db, log


router = APIRouter(prefix="/general_texts", tags=["Users General Texts"])


@router.get("/list", response_model=UsersFieldsListResponse)
async def get_fields_list(
        language: str,
):
    try:
        fields = await db.get_general_texts_by_language(language=language)
        return UsersFieldsListResponse(
            payload={
                field.field_id: field.text for field in fields
            }
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

