from datetime import datetime

from sqlmodel import Session
from fastapi.testclient import TestClient

from api.models import Order


def test_list_orders(session: Session, client: TestClient):
    order_1 = Order(
        asset='asset1',
        category='cat1',
        date=datetime.now(),
        operation_type='BUY',
        status='ACTIVE',
        value=100,
        value_fiat=100,
    )
    order_2 = Order(
        asset='asset2',
        category='cat2',
        date=datetime.now(),
        operation_type='BUY',
        status='ACTIVE',
        value=50,
        value_fiat=50,
    )
    session.add_all([order_1, order_2])
    session.commit()

    res = client.get('/orders/')
    data = res.json()

    print(data)
    assert res.status_code == 201
    assert len(data) == 2
    assert str(data[0]["id"]) == str(order_1.id)
    assert str(data[1]["id"]) == str(order_2.id)
