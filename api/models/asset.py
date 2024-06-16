from sqlmodel import Field
from typing import Optional

from api.utils import TimestamppedModel


class Asset(TimestamppedModel, table=True):
    id: Optional[int] = Field(primary_key=True, default=None)
    name: str = Field(nullable=False)
    code: str = Field(nullable=False)
    value: int = Field(nullable=False)
