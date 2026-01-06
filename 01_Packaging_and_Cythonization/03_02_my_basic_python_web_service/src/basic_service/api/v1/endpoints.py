from fastapi import APIRouter, BackgroundTasks
from basic_service.exceptions import AppException
from basic_service.logging_config import get_logger

from .dtos import (
    PromptRequest,
    PromptResponse,
    ResponseStatus,
    EngineeringApp,
)
from .service import generate_commands, audit_request

logger = get_logger("myEndpointLoggerName")

router = APIRouter(prefix="/api/v1/ava", tags=["ava"])


@router.post("/prompt", response_model=PromptResponse)
async def prompt(
    request: PromptRequest,
    background_tasks: BackgroundTasks,
) -> PromptResponse:
    logger.info(
        "Received prompt request",
        extra={
            "engineering_app": request.engineering_app,
            "query": request.user_query,
        },
    )

    if request.engineering_app == EngineeringApp.HYSYS:
        raise AppException("HYSYS is not supported", status_code=400)

    commands = await generate_commands(
        request.engineering_app,
        request.user_query,
    )

    background_tasks.add_task(
        audit_request,
        request.engineering_app,
        request.user_query,
        bool(commands),
    )

    if not commands:
        logger.info("No commands generated")
        return PromptResponse(
            status=ResponseStatus.FAIL,
            commands=[],
            message="No commands generated",
        )

    logger.info("Commands generated successfully")
    return PromptResponse(
        status=ResponseStatus.SUCCESS,
        commands=commands,
    )
