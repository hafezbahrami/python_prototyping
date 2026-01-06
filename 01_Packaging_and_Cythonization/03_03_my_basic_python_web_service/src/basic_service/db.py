from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from basic_service.config import APP_CONFIG

engine: AsyncEngine = create_async_engine(
    APP_CONFIG.database_url,
    echo=False,          # set True if you want SQL printed (can be noisy)
    pool_size=5,         # connection pool size (small for learning)
    max_overflow=5,      # allow temporary extra connections
)

SessionMaker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_session() -> AsyncSession:
    """
    Dependency that gives an endpoint a database session.
    FastAPI will create it per request, and we close it after.
    """
    async with SessionMaker() as session:
        yield session
