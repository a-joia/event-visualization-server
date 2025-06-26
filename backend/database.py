# Deprecated: All DB logic is now in db_provider.py. This file re-exports for backward compatibility.
from db_provider import engine, AsyncSessionLocal, Base, get_db, init_db

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from config import settings

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True, 
    future=True,
    pool_pre_ping=True
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine, 
    expire_on_commit=False, 
    class_=AsyncSession
)

# Create declarative base
Base = declarative_base()

# Dependency to get database session
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Initialize database tables
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) 