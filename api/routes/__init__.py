from fastapi import APIRouter

from .orders import router as order_router
from .plans import router as plan_router

main_router = APIRouter()


main_router.include_router(order_router, prefix="/orders", tags=["order"])
main_router.include_router(plan_router, prefix="/plans", tags=["plan"])
