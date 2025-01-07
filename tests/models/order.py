from datetime import datetime

from pytest import raises, mark
from sqlmodel import Session

from api.models import Order


@mark.asyncio
async def test_valid_with_values(session: Session):
    data = {
        "category": "crypto",
        "date": datetime.now(),
        "value": "1",
        "value_fiat": "100",
        "asset": "btc",
        "operation_type": "BUY",
        "status": "ACTIVE",
    }

    await Order.validate(data)
    db_order = Order(**data)

    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    order_dict = db_order.model_dump()

    for key in data.keys():
        assert str(data[key]) == str(order_dict[key])


@mark.asyncio
async def test_invalid_if_wrong_status():
    data = {
        "category": "crypto",
        "date": datetime.now(),
        "value": "1",
        "value_fiat": "100",
        "asset": "btc",
        "operation_type": "BUY",
        "status": "RANDOM",
    }

    with raises(ValueError):
        await Order.validate(data)


@mark.asyncio
async def test_invalid_if_wrong_operation_type():
    data = {
        "category": "crypto",
        "date": datetime.now(),
        "value": "1",
        "value_fiat": "100",
        "asset": "btc",
        "operation_type": "RANDOM",
        "status": "ACTIVE",
    }

    with raises(ValueError):
        await Order.validate(data)
