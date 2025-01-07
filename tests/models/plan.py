from datetime import datetime, timedelta

from pytest import raises, mark
from sqlmodel import Session

from api.models import Plan, PlanRequirement


@mark.asyncio
async def test_plan_valid_with_values(session: Session):
    data = {
        "name": 'plan 1',
        "total_value": 1000,
        "due_date": datetime.now(),
        "status": 'ACTIVE',
    }

    await Plan.validate(data)
    db_plan = Plan(**data)

    session.add(db_plan)
    session.commit()
    session.refresh(db_plan)

    plan_dict = db_plan.model_dump()

    for key in data.keys():
        assert str(data[key]) == str(plan_dict[key])


@mark.asyncio
async def test_plan_invalid_if_wrong_status():
    data = {
        "name": 'plan 1',
        "total_value": 1000,
        "due_date": datetime.now(),
        "status": 'RANDOM',
    }

    with raises(ValueError):
        await Plan.validate(data)


@mark.asyncio
async def test_plan_requirements_valid_with_values(session: Session):
    plan = Plan(name='plan 1', total_value=1000, due_date=datetime.now(), status='ACTIVE')
    session.add(plan)
    session.commit()
    session.refresh(plan)

    data = {"name": 'requirement 1', "description": 'description 1', "plan_id": plan.id}

    await PlanRequirement.validate(data)
    db_plan_requirement = PlanRequirement(**data)

    session.add(db_plan_requirement)
    session.commit()
    session.refresh(db_plan_requirement)

    plan_requirement_dict = db_plan_requirement.model_dump()

    for key in data.keys():
        assert str(data[key]) == str(plan_requirement_dict[key])


@mark.asyncio
async def test_plan_requirements_invalid_if_due_date_gt_plan_date(session: Session):
    plan = Plan(name='plan 1', total_value=1000, due_date=datetime.now(), status='ACTIVE')
    session.add(plan)
    session.commit()
    session.refresh(plan)

    data = {
        "name": 'requirement 1',
        "description": 'description 1',
        "plan_id": plan.id,
        "due_date": plan.due_date + timedelta(days=1),
    }

    with raises(ValueError):
        await PlanRequirement.validate(data, session)
