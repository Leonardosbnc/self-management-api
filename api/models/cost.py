from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field, Relationship

from api.utils import TimestamppedModel


class Cost(TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(nullable=False)
    value: int = Field(nullable=False)
    initial_date: datetime = Field(nullable=False)
    final_date: Optional[datetime] = Field(nullable=True)

    payments: list['Payment'] = Relationship(back_populates="cost")


class Payment(TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)

    cost_id: UUID = Field(foreign_key='cost.id')
    cost: Cost = Relationship(back_populates="payments")
