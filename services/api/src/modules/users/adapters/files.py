from aiobotocore.session import get_session
from botocore.exceptions import ClientError
from fastapi import UploadFile
from ....conf import settings
from logging import getLogger
from uuid import uuid4


class FileException(Exception):
    pass

logger = getLogger(__name__)


class FilesManager:

    def __init__(self):
        self.session = get_session()

    @staticmethod
    def _get_s3_url(bucket: str, key: str):
        return f'https://storage.yandexcloud.net/{bucket}/{key}'

    async def save_file(self, upload_file: UploadFile,
                        bucket: str,
                        folder: str
                        ) -> str:

        try:
            key = f'{folder}/{uuid4()}/{upload_file.filename}'

            async with self.session.create_client('s3',
                                                  endpoint_url='https://storage.yandexcloud.net',
                                                  region_name='ru-central1',
                                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY) as s3:

                response = await s3.put_object(Bucket=bucket, Key=key, Body=upload_file.file)
                logger.debug('File uploaded')
                return self._get_s3_url(bucket, key)
        except ClientError as e:
            logger.exception('Error uploading file %s' % upload_file, exc_info=e)
            raise FileException

    async def delete_file(self, bucket: str, key: str):
        try:
            async with self.session.create_client('s3',
                                                  endpoint_url='https://storage.yandexcloud.net',
                                                  region_name='ru-central1',
                                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY) as s3:
                response = await s3.delete_object(Bucket=bucket, Key=key)
                logger.debug('File deleted')
        except ClientError as e:
            logger.exception('Error deleting file', exc_info=e)
            raise FileException


file_manager = FilesManager()
