from uuid import UUID
from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CostDetailedResponse(BaseModel):
    id: UUID
    name: str
    value: int
    initial_date: datetime
    final_date: datetime

    payments: list['PaymentDetail']


class CostRequest(BaseModel):
    name: str
    value: int
    final_date: Optional[datetime]


class PaymentDetail(BaseModel):
    created_at: datetime


class PaymentRequest(BaseModel):
    cost_id: UUID
