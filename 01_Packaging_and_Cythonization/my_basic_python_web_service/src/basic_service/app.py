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
