import ydb

from .settings import Settings
from sqlmodel import Session
from ydb.iam.auth import YandexPassportOAuthIamCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings() # type: ignore
driver_config = ydb.DriverConfig(
    f'grpcs://{settings.DOCUMENT_API_ENDPOINT}', settings.DOCUMENT_DATABASE_PATH, credentials=YandexPassportOAuthIamCredentials(settings.OAUTH_KEY),
    root_certificates=ydb.load_ydb_root_certificate(),
)


driver = ydb.Driver(driver_config)
driver.wait(timeout=5)

engine = create_engine(settings.sqlalchemy_url, connect_args={
    "credentials": YandexPassportOAuthIamCredentials(settings.OAUTH_KEY),
    'protocol': 'grpcs'})

session_maker = sessionmaker(engine, expire_on_commit=False, class_=Session)


