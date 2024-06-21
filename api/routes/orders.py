from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select


from api.db import ActiveSession
from api.serializers import OrderRequest, OrderDetailedResponse
from api.models import Order

router = APIRouter()


@router.get("/", response_model=List[OrderDetailedResponse], status_code=200)
async def orders(*, session: Session = ActiveSession):
    orders = session.exec(select(Order)).all()
    return orders


@router.get("/{id}", response_model=OrderDetailedResponse, status_code=200)
async def order(*, id: UUID, session: Session = ActiveSession):
    order = session.exec(select(Order).where(Order.id == id)).first()

    if order is None:
        raise HTTPException(status_code=404)

    return order


@router.delete("/{id}", status_code=204)
async def delete_order(*, id: UUID, session: Session = ActiveSession):
    order = session.exec(select(Order).where(Order.id == id)).first()

    if order is None:
        raise HTTPException(status_code=404)

    session.delete(order)
    session.commit()

    return


@router.post("/", response_model=OrderDetailedResponse, status_code=201)
async def create_order(*, session: Session = ActiveSession, order: OrderRequest):
    db_order = Order.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
