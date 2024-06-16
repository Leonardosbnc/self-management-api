from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class PlanDetailedResponse(BaseModel):
    id: UUID
    name: str
    total_value: int
    due_date: datetime
    status: str

    requirements: list['PlanRequirementDetail']
    installments: list['PlanInstallmentDetail']


class PlanRequest(BaseModel):
    name: str
    total_value: int
    due_date: Optional[datetime]
    status: str


class PlanRequirementDetail(BaseModel):
    id: UUID
    name: str
    description: str
    due_date: datetime
    finished_at: datetime
    note: str


class PlanInstallmentDetail(BaseModel):
    id: UUID
    value: int


class PlanRequirementRequest(BaseModel):
    name: str
    description: str
    due_date: datetime
    finished_at: datetime
    note: str

    plan_id: UUID


class PlanInstallmentRequest(BaseModel):
    value: int

    plan_id: UUID
