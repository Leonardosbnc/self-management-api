from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class ReminderDetailedResponse(BaseModel):
    id: UUID
    name: str
    description: str
    date: datetime
    created_at: datetime


class ReminderRequest(BaseModel):
    name: str
    description: str
    date: datetime
