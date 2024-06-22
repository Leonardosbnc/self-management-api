import datetime

from uuid import UUID, uuid4
from typing import Optional
from sqlmodel import Field

from api.utils import TimestamppedModel, CustomValidateModel
from api.consts import ORDER_OPERATIONS, STATUS


class Order(CustomValidateModel, TimestamppedModel, table=True):
    id: UUID = Field(primary_key=True, nullable=False, default_factory=uuid4)
    category: str = Field(nullable=False)
    description: Optional[str] = Field(nullable=True)
    date: datetime.datetime = Field(nullable=False)
    value: int = Field(nullable=False)
    value_fiat: int = Field(nullable=False)
    asset: str = Field(nullable=False)
    operation_type: str = Field(nullable=False)
    status: str = Field(nullable=False)

    @classmethod
    async def validate(cls, obj):
        if obj["operation_type"] not in ORDER_OPERATIONS:
            raise ValueError(f'Operation Type must be one of the following {ORDER_OPERATIONS}')

        if obj["status"] not in STATUS:
            raise ValueError(f'Status must be one of the following {STATUS}')
