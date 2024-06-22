from datetime import datetime
from sqlmodel import SQLModel, Field


class TimestamppedModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CustomValidateModel(SQLModel):
    @classmethod
    async def validate(self, obj):
        raise NotImplementedError()

    @classmethod
    async def model_validate(cls, obj, **kwargs):
        await cls.validate(dict(obj))

        return super().model_validate(obj=obj, **kwargs)
