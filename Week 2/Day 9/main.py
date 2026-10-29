import time
import uuid
import logging
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.background import BackgroundTask

# Setup clean, simple loggingost
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api")



def simple_audit_task(request_id: str):

    logger.info(f"[AUDIT TASK COMPLETED] Logged for ID: {request_id}")


class RequestTimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        start_time = time.time()

        
        headers = dict(request.headers)
        if "authorization" in headers:
            headers["authorization"] = "[REDACTED]"

        logger.info(f"START: {request.method} {request.url.path} | ID: {request_id}")

        
        response = await call_next(request)

        # Calculate time taken
        duration = (time.time() - start_time) * 1000
        logger.info(f"END: Status {response.status_code} | Took {duration:.2f}ms | ID: {request_id}")

        # Send trace ID back to client via headers
        response.headers["X-Request-ID"] = request_id

        # Attach the background audit action to the response object
        response.background = BackgroundTask(simple_audit_task, request_id=request_id)

        return response

async def universal_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": {
                "message": "A system error occurred.",
                "details": str(exc)
            }  
        }
    )
async def success_route(request: Request):
    return JSONResponse({"status": "ok", "message": "Success!"})

async def crash_route(request: Request):
    # Intentional crash to trigger our exception handler
    return 1 / 0

# List routes
routes = [
    Route("/success", endpoint=success_route, methods=["GET"]),
    Route("/crash", endpoint=crash_route, methods=["GET"])
]


middleware = [
    Middleware(RequestTimerMiddleware)
]


exception_handlers = {
    500: universal_error_handler,
    Exception: universal_error_handler
}

# Combine everything cleanly inside Starlette
app = Starlette(
    routes=routes, 
    middleware=middleware, 
    exception_handlers=exception_handlers
)
