from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from basic_service.db import get_session
from basic_service.exceptions import AppException
from .dtos import PromptRequest, PromptResponse, EngineeringApp, PromptHistoryResponse, PromptHistoryItem
from .service import handle_prompt
from .repository import get_prompt_history

router = APIRouter(prefix="/api/v1/ava", tags=["ava"])

@router.post("/prompt", response_model=PromptResponse)
async def prompt(
    request: PromptRequest,
    session: AsyncSession = Depends(get_session),
) -> PromptResponse:
    if request.engineering_app == EngineeringApp.HYSYS:
        raise AppException("HYSYS is not supported", 400)

    status, commands = await handle_prompt(session, request.engineering_app, request.user_query)

    if not commands:
        return PromptResponse(status=status, commands=[], message="No commands generated")

    return PromptResponse(status=status, commands=commands, message="")


@router.get("/history", response_model=PromptHistoryResponse)
async def history(
    limit: int = 20,
    session: AsyncSession = Depends(get_session),
) -> PromptHistoryResponse:
    rows = await get_prompt_history(session, limit=limit)

    items = [
        PromptHistoryItem(
            id=r.id,
            engineering_app=r.engineering_app,
            user_query=r.user_query,
            status=r.status,
            created_at=str(r.created_at),
        )
        for r in rows
    ]
    return PromptHistoryResponse(items=items)
