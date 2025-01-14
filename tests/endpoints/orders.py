from datetime import datetime

from sqlmodel import Session, select
from fastapi.testclient import TestClient

from api.models import Order

default_order_data = {
    "category": "crypto",
    "date": str(datetime.now()),
    "value": "1",
    "asset": "btc",
    "operation_type": "BUY",
    "status": "ACTIVE",
}


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

    assert res.status_code == 200
    assert len(data) == 2
    assert str(data[0]["id"]) == str(order_1.id)
    assert str(data[1]["id"]) == str(order_2.id)


def test_retrieve_order(session: Session, client: TestClient):
    order = Order(
        asset='asset1',
        category='cat1',
        date=datetime.now(),
        operation_type='BUY',
        status='ACTIVE',
        value=100,
        value_fiat=100,
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    res = client.get(f'/orders/{order.id}')
    data = res.json()

    assert res.status_code == 200
    assert str(data["id"]) == str(order.id)
    assert data["category"] == order.category


def test_create_order(session: Session, client: TestClient):
    res = client.post(
        '/orders/',
        json={
            **default_order_data,
            "value_fiat": "100",
        },
    )
    data = res.json()
    db_order = session.exec(select(Order)).first()

    assert res.status_code == 201
    assert str(data["id"]) == str(db_order.id)


def test_error_if_miss_required_field_on_create_order(_, client: TestClient):
    res = client.post('/orders/', json=default_order_data)

    assert res.status_code == 422


def test_delete_order(session: Session, client: TestClient):
    order = Order(
        asset='asset1',
        category='cat1',
        date=datetime.now(),
        operation_type='BUY',
        status='ACTIVE',
        value=100,
        value_fiat=100,
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    res = client.delete(f'/orders/{order.id}')

    orders = session.exec(select(Order)).all()

    assert res.status_code == 204
    assert len(orders) == 0


def test_update_order(session: Session, client: TestClient):
    order = Order(
        asset='asset1',
        category='cat1',
        date=datetime.now(),
        operation_type='BUY',
        status='ACTIVE',
        value=100,
        value_fiat=100,
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    update_data = {"status": 'COMPLETED', "description": 'test description', "category": 'cat test'}

    res = client.patch(
        f'/orders/{order.id}',
        json=update_data,
    )

    session.refresh(order)

    assert res.status_code == 200

    for k, v in update_data.items():
        assert v == getattr(order, k)
