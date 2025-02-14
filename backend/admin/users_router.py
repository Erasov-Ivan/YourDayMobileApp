from fastapi import APIRouter
from schemas import *
from . import db, log, DATE_FORMAT, encode_jwt_token


router = APIRouter(prefix="/users", tags=["Admin Users"])


@router.get("/list", response_model=UserListResponse)
async def get_user_list(
        limit: int = 10,
        offset: int = 0,
):
    try:
        users = await db.get_users(limit=limit, offset=offset)
        total_count = await db.count_users()
        return UserListResponse(
            payload=UserListModel(
                total_count=total_count,
                users=[
                    UserModel(
                        id=user.id,
                        email=user.email,
                        token=await encode_jwt_token(data=f'{user.id}:{user.email}'),
                        name=user.name,
                        bdate=user.bdate.strftime(DATE_FORMAT),
                        approved=user.approved,
                        current_code=user.current_code
                    ) for user in users
                ]
            )
        )
    except Exception as e:
        log.error(str(e))
        return BaseResponse(error=True, message=str(e))

