"""
HTTP Latency Timing, Security Headers, and Exception Handler Middlewares.
"""
import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, JSONResponse
from app.core.exceptions import AppBaseException

logger = logging.getLogger("app.core.middleware")

class ProcessTimerAndSecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        try:
            response: Response = await call_next(request)
        except AppBaseException as e:
            logger.warning(f"App exception on {request.method} {request.url.path}: {e.message}")
            return JSONResponse(
                status_code=e.status_code,
                content={
                    "success": False,
                    "error": e.message,
                    "details": e.details,
                    "status_code": e.status_code
                }
            )
        except Exception as exc:
            logger.exception(f"Unhandled server error on {request.method} {request.url.path}: {str(exc)}")
            return JSONResponse(
                status_code=500,
                content={
                    "success": False,
                    "error": "An unexpected error occurred. Please try again later.",
                    "status_code": 500
                }
            )
        
        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response
