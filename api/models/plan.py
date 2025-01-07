import datetime

from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, Relationship, select, Session

from api.utils import TimestamppedModel, CustomValidateModel
from api.consts import STATUS
from api.db import engine


class Plan(CustomValidateModel, TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(nullable=False)
    total_value: int = Field(nullable=False)
    due_date: Optional[datetime.datetime] = Field(nullable=True)
    status: str = Field(nullable=False)

    requirements: list['PlanRequirement'] = Relationship(back_populates="plan")
    installments: list['PlanInstallment'] = Relationship(back_populates="plan")

    @classmethod
    async def validate(cls, obj):
        if obj["status"] not in STATUS:
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

    @classmethod
    async def validate(cls, obj: dict, session=None):
        obj.setdefault('due_date', None)
        query = select(Plan).where(Plan.id == obj["plan_id"])

        if session is None:
            with Session(engine) as _session:
                plan = _session.exec(query).first()
        else:
            plan = session.exec(query).first()

        if (
            obj["due_date"] is not None
            and plan.due_date is not None
            and obj["due_date"] > plan.due_date
        ):
            raise ValueError('Requirement due_date cannot be greater than plan due_date')


class PlanInstallment(TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    value: int = Field(nullable=False)

    plan_id: UUID = Field(foreign_key='plan.id')
    plan: Plan = Relationship(back_populates="installments")
