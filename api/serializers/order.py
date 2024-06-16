from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class OrderDetailedResponse(BaseModel):
    id: UUID
    category: str
    description: str
    date: datetime
    value: int
    value_fiat: int
    asset: str
    operation_type: str
    status: str


class OrderRequest(BaseModel):
    category: str
    description: Optional[str]
    date: datetime
    value: int
    value_fiat: int
    asset: str
    operation_type: str
    status: str
