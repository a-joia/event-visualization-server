"""
Database Provider Module
-----------------------
This module centralizes all database engine, session, and base management.
To switch database backends (SQLite, PostgreSQL, MySQL, etc.), only update this file and the DATABASE_URL in config.py.
"""

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from config import settings

# Create async engine (change DATABASE_URL in config.py to switch DB backend)
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

# Declarative base for models
Base = declarative_base()

# Dependency to get DB session (for FastAPI DI)
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

# Initialize database tables (call on startup or via script)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# --- Usage in the rest of the app ---
# from db_provider import engine, AsyncSessionLocal, Base, get_db, init_db
#
# - Use Base for model definitions
# - Use get_db as FastAPI dependency
# - Use init_db for migrations or startup 