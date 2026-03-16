from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def liveness() -> dict[str, object]:
    return {"message": "ok", "data": {"service": "api", "status": "alive"}}
