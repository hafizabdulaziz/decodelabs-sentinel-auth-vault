import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app

# Database URL for testing
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/test_db"

@pytest_asyncio.fixture(scope="session")
async def db_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    connection = await db_engine.connect()
    transaction = await connection.begin()
    session = sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)()
    
    yield session
    
    await session.close()
    await transaction.rollback()
    await connection.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    def _get_test_db():
        yield db_session
    
    app.dependency_overrides[app.dependency_overrides.get("get_db", "app.db.session.get_db")] = _get_test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
