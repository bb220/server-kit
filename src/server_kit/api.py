from fastapi import APIRouter

from server_kit.routers import customers_router

router = APIRouter()


@router.get("/health")
async def liveness() -> dict[str, object]:
    return {"message": "ok", "data": {"service": "api", "status": "alive"}}


router.include_router(customers_router)
