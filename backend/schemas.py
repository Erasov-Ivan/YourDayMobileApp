from typing import Any, Optional, List
from pydantic import BaseModel


class BaseResponse(BaseModel):
    error: bool = False
    message: str = 'OK'
    payload: Optional[Any] = None


class UserModel(BaseModel):
    id: int
    email: str
    token: Optional[str]
    name: str
    bdate: str
    approved: bool
    current_code: Optional[str]


class UserListModel(BaseModel):
    total_count: int
    users: List[UserModel] = []


class UserListResponse(BaseResponse):
    payload: Optional[UserListModel] = None


class TextModel(BaseModel):
    language: str
    text: str


class FieldModel(BaseModel):
    id: str
    description: str
    texts: list[TextModel] = []


class FieldsListModel(BaseModel):
    total_count: int
    fields: List[FieldModel] = []


class FieldsListResponse(BaseResponse):
    payload: Optional[FieldsListModel] = None


class UsersFieldsListResponse(BaseResponse):
    payload: Optional[dict[str, str]] = None


class SubscriptionModel(BaseModel):
    id: str
    description: str


class SubscriptionListModel(BaseModel):
    subscriptions: List[SubscriptionModel] = []


class SubscriptionsListResponse(BaseResponse):
    payload: Optional[SubscriptionListModel] = None
