from fastapi import APIRouter, Request, Response, status

from server_kit.db import check_database_connection

from server_kit.routers import customers_router

router = APIRouter()


@router.get("/health")
async def liveness(request: Request, response: Response) -> dict[str, object]:
    database_ready = await check_database_connection(request.app.state.db_engine)
    response_body = {
        "message": "ok" if database_ready else "degraded",
        "data": {
            "service": "api",
            "status": "alive",
            "database": "ready" if database_ready else "unavailable",
        },
    }

    if not database_ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return response_body


router.include_router(customers_router)
