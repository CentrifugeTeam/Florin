from .settings import Settings
from sqlmodel.ext.asyncio.session import AsyncSession
from ydb.aio.iam import YandexPassportOAuthIamCredentials
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

settings = Settings() # type: ignore
engine = create_async_engine(settings.sqlalchemy_url, connect_args={
    "credentials": YandexPassportOAuthIamCredentials(settings.OAUTH_KEY),
    'protocol': 'grpcs'})
#???
session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)




