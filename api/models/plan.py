import datetime

from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, Relationship

from api.utils import TimestamppedModel, CustomValidateModel
from api.consts import STATUS


class Plan(CustomValidateModel, TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(nullable=False)
    total_value: int = Field(nullable=False)
    due_date: Optional[datetime.datetime] = Field(nullable=True)
    status: str = Field(nullable=False)

    requirements: list['PlanRequirement'] = Relationship(back_populates="plan")
    installments: list['PlanInstallment'] = Relationship(back_populates="plan")

    def validate(self):
        if self.status not in STATUS:
            raise ValueError(f'Status must be one of the following {STATUS}')


class PlanRequirement(CustomValidateModel, TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    due_date: Optional[datetime.datetime] = Field(nullable=True)
    finished_at: Optional[datetime.datetime] = Field(nullable=True)
    note: Optional[str] = Field(nullable=True)

    plan_id: UUID = Field(foreign_key='plan.id')
    plan: Plan = Relationship(back_populates="requirements")

    def validate(self):
        if (
            self.due_date is not None
            and self.plan.due_date is not None
            and self.due_date > self.plan.due_date
        ):
            raise ValueError('Requirement due_date cannot be greater than plan due_date')


class PlanInstallment(TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    value: int = Field(nullable=False)

    plan_id: UUID = Field(foreign_key='plan.id')
    plan: Plan = Relationship(back_populates="installments")
