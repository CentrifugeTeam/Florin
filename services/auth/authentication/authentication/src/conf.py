import ydb

from .settings import Settings
from ydb.iam.auth import YandexPassportOAuthIamCredentials

settings = Settings() # type: ignore
driver_config = ydb.DriverConfig(
    f'grpcs://{settings.DOCUMENT_API_ENDPOINT}', settings.DOCUMENT_DATABASE_PATH, credentials=YandexPassportOAuthIamCredentials(settings.OAUTH_KEY),
    root_certificates=ydb.load_ydb_root_certificate(),
)


driver = ydb.Driver(driver_config)
driver.wait(timeout=5)
