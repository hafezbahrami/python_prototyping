import asyncio
from .dtos import EngineeringApp
from basic_service.logging_config import get_logger

logger = get_logger("service")


async def generate_commands(app: EngineeringApp, query: str) -> list[str]:
    logger.debug("Starting command generation")
    await asyncio.sleep(0.2)

    if app.name == "HYSYS":
        return []

    return [
        f"SET COMPONENT FROM QUERY: {query}",
        "RUN SIMULATION",
    ]


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
