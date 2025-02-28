from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn
from pathlib import Path


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='postgres_')
    username: str = Field(validation_alias='postgres_user')
    password: str
    host: str
    port: int
    db: str

    @property
    def sqlalchemy_url(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.username,
                password=self.password,
                host=self.host,
                port=self.port,
                path=self.db,
            )
        )


class MinioSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix='minio_')
    access_key: str
    secret_key: str
    endpoint: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra='allow')
    JWT_PRIVATE_KEY: str
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    minio: MinioSettings = Field(default_factory=MinioSettings)
