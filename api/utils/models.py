from datetime import datetime
from sqlmodel import SQLModel, Field


class TimestamppedModel(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class CustomValidateModel(SQLModel):
    def validate(self):
        raise NotImplementedError()

    @classmethod
    def model_validate(cls, **kwargs):
        obj = kwargs.pop('obj')
        obj.validate()

        return super().model_validate(obj=obj, **kwargs)
