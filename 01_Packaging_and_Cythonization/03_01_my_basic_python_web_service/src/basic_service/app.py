from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from basic_service.config import APP_CONFIG
from basic_service.api.v1.endpoints import router
from basic_service.exceptions import AppException


app = FastAPI(
    title=APP_CONFIG.app_name,
    version=APP_CONFIG.app_version,
)


@app.exception_handler(AppException)
def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


app.include_router(router)


if APP_CONFIG.is_dev:
    @app.get("/")
    def root():
        return {"message": "Development mode is ON"}



# -------------------------------------------------------------------------------
# ------ For Debugging ----------------------------------------------------------
# -------------------------------------------------------------------------------

if APP_CONFIG.is_dev:

    @app.middleware("http")
    async def debug_request_middleware(request: Request, call_next):
        """
        Development-only middleware to inspect incoming HTTP requests (inspect bytes and headers).
        """

        # ---- HTTP metadata ----
        method = request.method
        path = request.url.path
        headers = dict(request.headers)

        # ---- Raw body bytes ----
        body_bytes = await request.body()

        # SET BREAKPOINT HERE
        debug_snapshot = {
            "method": method,
            "path": path,
            "content_type": headers.get("content-type"),
            "body_bytes": body_bytes,
            "body_as_text": body_bytes.decode("utf-8", errors="replace"),
        }

        # IMPORTANT:
        # Re-inject the body so downstream (FastAPI/Pydantic) can read it
        async def receive():
            return {
                "type": "http.request",
                "body": body_bytes,
                "more_body": False,
            }

        request._receive = receive  # dev-only internal override

        response = await call_next(request)

        # OPTIONAL BREAKPOINT HERE
        response_debug = {
            "status_code": response.status_code,
            "headers": dict(response.headers),
        }

        return response

