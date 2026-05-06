"""
Application middleware registration
"""

import logging
import time

from fastapi import FastAPI, Request

logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """Log request method, path, and response time"""
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time

    logger.info(
        "%s %s — %d (%.3fs)",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    response.headers["X-Process-Time"] = str(duration)
    return response


def register_middleware(app: FastAPI) -> None:
    """Register all custom middleware"""
    app.middleware("http")(log_requests)
