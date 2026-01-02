from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from basic_service.config import APP_CONFIG
from basic_service.exceptions import AppException
from basic_service.api.v1.endpoints import router

from basic_service.logging_config import get_logger

logger = get_logger("debug")

app = FastAPI(
    title="Basic Educational Web Service",
    version="0.2.0",
)

# -------------------------------------------------------------------------------

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.message},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # validation failures (incoming http request (the msin body) does not comply with the paydantic object
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

app.include_router(router)

# -------------------------------------------------------------------------------

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
        # A) request line basics
        method = request.method
        path = request.url.path
        query_string = request.url.query

        # B) headers (note: values are strings)
        headers = dict(request.headers)

        # C) raw body bytes (this is the closest to "wire format" you'll see in app code)
        body_bytes = await request.body()
        body_text = body_bytes.decode("utf-8", errors="replace")

        # D) OPTIONAL: try parse JSON in middleware (educational; FastAPI will also parse later)
        parsed_json = None
        json_error = None
        if headers.get("content-type", "").startswith("application/json") and body_text.strip():
            try:
                import json
                parsed_json = json.loads(body_text)
            except Exception as e:
                json_error = repr(e)

        # "incoming request snapshot"
        incoming = {
            "method": method,
            "path": path,
            "query_string": query_string,
            "content_type": headers.get("content-type"),
            "x_debug_user": headers.get("x-debug-user"),
            "body_bytes": body_bytes,
            "body_text": body_text,
            "parsed_json": parsed_json,
            "json_error": json_error,
        }

        # IMPORTANT: re-inject the body so FastAPI/Pydantic can read it downstream
        async def receive():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request._receive = receive  # dev-only hack

        # E) pass control onward (routing + validation + endpoint)
        response = await call_next(request)

        # "outgoing response snapshot"
        outgoing = {
            "status_code": response.status_code,
            "response_headers": dict(response.headers),
        }

        logger.debug("request_debug", extra={"incoming": incoming, "outgoing": outgoing})
        return response