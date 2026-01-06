from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from .models import PromptLog

async def insert_prompt_log(
    session: AsyncSession,
    engineering_app: str,
    user_query: str,
    status: str,
) -> PromptLog:
    row = PromptLog(engineering_app=engineering_app, user_query=user_query, status=status)
    session.add(row)
    await session.commit()          # transaction commit (writes)
    await session.refresh(row)      # get auto-generated fields like id
    return row

async def get_prompt_history(session: AsyncSession, limit: int) -> list[PromptLog]:
    stmt = select(PromptLog).order_by(desc(PromptLog.id)).limit(limit)
    result = await session.execute(stmt)
    return list(result.scalars().all())
