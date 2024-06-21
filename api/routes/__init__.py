from fastapi import APIRouter

from .orders import router as order_router

main_router = APIRouter()


main_router.include_router(order_router, prefix="/orders", tags=["order"])
