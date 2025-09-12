from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.settings import settings


engine = create_async_engine(
	settings.DATABASE_URL,
	echo=settings.DEBUG,
	pool_size=20,
	max_overflow=30,
	pool_pre_ping=True,
	pool_recycle=3600,
)

SessionLocal = sessionmaker(
	engine, 
	class_=AsyncSession, 
	autocommit=False, 
	autoflush=False,
	expire_on_commit=False
)

async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session

