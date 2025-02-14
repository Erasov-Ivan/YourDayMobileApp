from . import db, decode_jwt_token
from models import *


async def get_user_by_token(token: str) -> User:
    data = await decode_jwt_token(token=token)
    user_id, email = data.split(':')
    user_id = int(user_id)
    users = await db.get_users_from_token(user_id=user_id, email=email)
    if len(users) == 0:
        raise Exception('No users found')
    else:
        user = users[0]
        return user

