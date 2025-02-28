from fastapi import UploadFile, HTTPException, status
from ...conf import settings
from logging import getLogger
from uuid import uuid4
from minio import Minio


class FileException(Exception):
    pass


FileDoesntSavedResponse = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Can't save a file")

logger = getLogger(__name__)


class FileAdapter:

    def __init__(self):
        self.client = Minio(settings.minio.endpoint,
                            access_key=settings.minio.access_key,
                            secret_key=settings.minio.secret_key)

    @staticmethod
    def _get_s3_url(bucket: str, key: str):
        return f'http://158.160.39.75/api/files/download/{bucket}/{key}'

    def get_file(self, bucket_name: str, object_name: str):
        res = self.client.get_object(
            bucket_name=bucket_name, object_name=object_name)
        if res.status == 200:
            return res.data
        if res.status == 404:
            raise HTTPException(status_code=404)
        raise HTTPException(status_code=500, detail=res.reason)

    def save_file(self, upload_file: UploadFile,
                  bucket_name: str,
                  ) -> str:

        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)

        try:
            result = self.client.put_object(
                bucket_name, upload_file.filename, upload_file.file.read(), upload_file.size)
        except Exception as e:
            raise FileDoesntSavedResponse

        return f"{result.bucket_name}/{result.object_name}"

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


adapter = FileAdapter()
