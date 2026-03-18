from contextlib import asynccontextmanager
from time import perf_counter_ns
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request

from server_kit.api import router
from server_kit.db import (
    create_database_engine,
    create_session_factory,
    dispose_database_engine,
)
from server_kit.logging import configure_logging, get_logger
from server_kit.settings import Settings, get_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.state.settings
    configure_logging(settings)
    app.state.db_engine = create_database_engine(settings)
    app.state.session_factory = create_session_factory(app.state.db_engine)

    logger.info(
        "app.startup",
        log_format=settings.log_format,
    )
    yield
    await dispose_database_engine(app.state.db_engine)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings

    @app.middleware("http")
    async def bind_request_logging_context(request: Request, call_next):
        started_at_ns = perf_counter_ns()
        structlog.contextvars.clear_contextvars()
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        request.state.request_id = request_id
        structlog.contextvars.bind_contextvars(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
        )

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (perf_counter_ns() - started_at_ns) / 1_000_000
            logger.exception(
                "http.request.failed",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=500,
                duration_ms=duration_ms,
            )
            raise

        duration_ms = (perf_counter_ns() - started_at_ns) / 1_000_000
        logger.info(
            "http.request.completed",
            status_code=response.status_code,
            duration_ms=duration_ms,
        )
        response.headers["X-Request-ID"] = request_id
        try:
            return response
        finally:
            structlog.contextvars.clear_contextvars()

    app.include_router(router)
    return app


app = create_app()
