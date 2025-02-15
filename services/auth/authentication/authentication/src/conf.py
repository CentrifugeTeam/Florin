from settings import Settings
from sqlmodel import Session
from ydb.iam.auth import YandexPassportOAuthIamCredentials
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

settings = Settings() # type: ignore
engine = create_engine(settings.sqlalchemy_url, connect_args={
    "credentials": YandexPassportOAuthIamCredentials(settings.OAUTH_KEY),
    'protocol': 'grpcs'})

session_maker = sessionmaker(engine, expire_on_commit=False, class_=Session)



