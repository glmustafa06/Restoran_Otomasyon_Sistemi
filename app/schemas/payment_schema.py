"""
Ödeme Schema'ları
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    tip: float = 0

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
