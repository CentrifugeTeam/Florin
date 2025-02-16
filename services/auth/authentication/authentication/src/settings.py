from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

path = Path(__file__).parent.parent / '.env'

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=path, extra='allow')
    OAUTH_KEY: str
    DOCUMENT_API_ENDPOINT: str
    DOCUMENT_DATABASE_PATH: str
    JWT_PRIVATE_KEY: str

    @property
    def sqlalchemy_url(self):
        return f"yql+ydb://{self.DOCUMENT_API_ENDPOINT}{self.DOCUMENT_DATABASE_PATH}"
