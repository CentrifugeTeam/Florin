from .settings import Settings
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from redis.asyncio import ConnectionPool

settings = Settings()  # type: ignore
engine = create_async_engine(settings.database.sqlalchemy_url)
session_maker = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession)

connection_pool = ConnectionPool(
    host=settings.redis.host, port=settings.redis.port, decode_responses=True)
