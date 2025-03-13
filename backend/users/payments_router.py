from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import hashlib
import logging
import datetime
from . import ROBOKASSA_MERCHANT_LOGIN, ROBOKASSA_PASSWORD, db
from .utils import process_payment, get_user_by_token
from schemas import BaseResponse

router = APIRouter(prefix="/payments", tags=["Users Payments"])


def calculate_signature(*args) -> str:
    return hashlib.md5(':'.join(str(arg) for arg in args).encode()).hexdigest()


@router.get("/generate_invoice_id", response_model=BaseResponse)
async def generate_invoice_id(
        token: str,
        cost: int
):
    try:
        user = await get_user_by_token(token=token)
        invoice_id = await db.new_invoice(user_id=user.id, cost=cost)
        return BaseResponse(error=False, message='OK', payload=invoice_id)
    except Exception as e:
        logging.error(e)
        return BaseResponse(error=True, message="Error")


@router.post("/robokassa_success")
async def robokassa_success(request: Request):
    form_data = await request.form()
    invoice_id = form_data.get("InvId")
    cost = form_data.get("OutSum")
    signature = form_data.get("SignatureValue")
    user_email = form_data.get("Shp_email")
    months = form_data.get("Shp_months")
    subscription = form_data.get("Shp_subscription")
    expected_signature = calculate_signature(
        cost,
        invoice_id,
        ROBOKASSA_PASSWORD,
        f'Shp_email={user_email}',
        f'Shp_months={months}',
        f'Shp_subscription={subscription}'
    )
    print(signature)
    print(expected_signature)
    if signature.lower() != expected_signature.lower():
        raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        await process_payment(
            user_email=user_email,
            subscription=subscription,
            months=int(months),
            cost=int(cost)
        )
        await db.approve_invoice(invoice_id=int(invoice_id))
        return f"OK{invoice_id}"
