from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import hashlib
from config import ROBOKASSA_MERCHANT_LOGIN, ROBOKASSA_PASSWORD

router = APIRouter(prefix="/payments", tags=["Users Payments"])


class PaymentRequest(BaseModel):
    amount: float
    description: str
    invoice_id: int


def generate_signature(amount: float, invoice_id: int, password: str) -> str:
    signature_string = f"{ROBOKASSA_MERCHANT_LOGIN}:{amount}:{invoice_id}:{password}"
    return hashlib.md5(signature_string.encode()).hexdigest()


@router.post("/robokassa_success")
async def robokassa_success(request: Request):
    try:
        print('request')
        print(request)
    except:
        pass
    try:
        print('request.json')
        print(request.json())
        print(await request.json())
    except:
        pass
    try:
        print('request.form')
        print(request.form())
        print(await request.form())
    except:
        pass
    invoice_id = 2
    try:
        form_data = await request.form()
        invoice_id = form_data.get("InvId")
        amount = form_data.get("OutSum")
        signature = form_data.get("SignatureValue")

        expected_signature = generate_signature(float(amount), int(invoice_id), ROBOKASSA_PASSWORD)
        print(signature)
        print(expected_signature)
        if signature.lower() != expected_signature.lower():
            raise HTTPException(status_code=400, detail="Invalid signature")
    except Exception as e:
        print(str(e))
    return f"OK{invoice_id}"
