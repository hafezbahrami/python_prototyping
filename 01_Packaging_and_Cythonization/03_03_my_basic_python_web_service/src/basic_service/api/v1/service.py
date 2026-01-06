import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from .dtos import EngineeringApp, ResponseStatus
from basic_service.logging_config import get_logger

from .repository import insert_prompt_log


logger = get_logger("myServiceLogName")


async def generate_commands(app: EngineeringApp, query: str) -> list[str]:
    logger.debug("Starting command generation")
    
    logger.debug("generate_commands: start")
    await asyncio.sleep(0.2)
    logger.debug("generate_commands: after await")

    if app.name == "HYSYS":
        return []

    return [
        f"SET COMPONENT FROM QUERY: {query}",
        "RUN SIMULATION",
    ]



async def handle_prompt(session: AsyncSession, app: EngineeringApp, query: str):
    commands = await generate_commands(app, query)

    status = ResponseStatus.SUCCESS if commands else ResponseStatus.FAIL

    await insert_prompt_log(
        session=session,
        engineering_app=app.value,
        user_query=query,
        status=status.value,
    )

    return status, commands


def audit_request(
    app: EngineeringApp,
    query: str,
    success: bool,
) -> None:
    """
    Runs after the response is sent.
    """
    logger.info(
        "Audit log",
        extra={
            "app": app.value,
            "query": query,
            "success": success,
        },
    )
