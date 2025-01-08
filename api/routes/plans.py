from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select


from api.db import ActiveSession
from api.serializers import PlanDetailedResponse, PlanRequest
from api.models import Plan

router = APIRouter()


@router.get("/", response_model=List[PlanDetailedResponse], status_code=200)
async def plans(*, session: Session = ActiveSession):
    orders = session.exec(select(Plan)).all()
    return orders
