from fastapi import APIRouter

from .dtos import HealthResponse, EchoRequest, EchoResponse
from basic_service.config import APP_CONFIG

router = APIRouter(prefix="/api/v1", tags=["v1"])


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        environment=APP_CONFIG.env,
    )


@router.post("/echo", response_model=EchoResponse)
def echo(request: EchoRequest) -> EchoResponse:
    return EchoResponse(
        echoed_message=request.message
    )
