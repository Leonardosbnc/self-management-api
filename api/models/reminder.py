from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field

from api.utils import TimestamppedModel


class Reminder(TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    name: str = Field(nullable=False)
    description: str = Field(nullable=True)
    date: datetime = Field(nullable=False)
