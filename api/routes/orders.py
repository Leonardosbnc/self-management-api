from typing import List
from uuid import UUID

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select


from api.db import ActiveSession
from api.serializers import OrderRequest, OrderDetailedResponse, OrderUpdate
from api.models import Order

router = APIRouter()


@router.get("/", response_model=List[OrderDetailedResponse], status_code=200)
async def orders(*, session: Session = ActiveSession):
    orders_data = session.exec(select(Order)).all()
    return orders_data


@router.get("/{order_id}", response_model=OrderDetailedResponse, status_code=200)
async def get_order_by_id(*, order_id: UUID, session: Session = ActiveSession):
    order_data = session.get(Order, order_id)

    if order_data is None:
        raise HTTPException(status_code=404)

    return order_data


@router.patch("/{order_id}", response_model=OrderDetailedResponse, status_code=200)
async def update_order(
    *,
    order_id: UUID,
    order: OrderUpdate,
    session: Session = ActiveSession,
):
    db_order = session.get(Order, order_id)

    if db_order is None:
        raise HTTPException(status_code=404)

    order_data = order.model_dump(exclude_unset=True)

    for k, v in order_data.items():
        setattr(db_order, k, v)

    try:
        await Order.validate(db_order.model_dump())

        session.commit()
        session.refresh(db_order)

        return db_order
    except ValueError as err:
        raise HTTPException(status_code=422, detail=str(err)) from err


@router.delete("/{order_id}", status_code=204)
async def delete_order(*, order_id: UUID, session: Session = ActiveSession):
    order = session.get(Order, order_id)

    if order is None:
        raise HTTPException(status_code=404)

    session.delete(order)
    session.commit()

    return


@router.post("/", response_model=OrderDetailedResponse, status_code=201)
async def create_order(*, session: Session = ActiveSession, order: OrderRequest):
    db_order = await Order.model_validate(order)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order
