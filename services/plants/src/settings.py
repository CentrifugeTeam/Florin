from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

path = Path(__file__).parent.parent / '.env'


class Settings(BaseSettings):
    
    @property
    def sqlalchemy_url(self):
        return f"sql+asyncydb://{self.DOCUMENT_API_ENDPOINT}{self.DOCUMENT_DATABASE_PATH}"
