from main import app
from sqlmodel.ext.asyncio.session import AsyncSession
from src.deps import get_session
from src.conf import engine
from contextlib import asynccontextmanager
from httpx import ASGITransport, AsyncClient
import pytest

pytestmark = pytest.mark.asyncio


@pytest.fixture()
def nice():
    return 1


@pytest.fixture()
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac


async def _session():
    async with engine.connect() as connection:
        async with connection.begin() as transaction:
            async_session = AsyncSession(
                bind=connection,
                join_transaction_mode="create_savepoint",
                expire_on_commit=False,
            )
            async with async_session as session:
                yield session

            await transaction.rollback()


@pytest.fixture()
async def session():
    async with asynccontextmanager(_session)() as ctx:
        async def wrapper():
            return ctx
        app.dependency_overrides[get_session] = wrapper
        yield ctx
