from fastapi import UploadFile, HTTPException, status
from fastapi.concurrency import run_in_threadpool
from ...conf import settings
from logging import getLogger
from uuid import uuid4
from minio import Minio
from minio.error import MinioException


class FileException(Exception):
    pass


FileDoesntSavedResponse = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Can't save a file"
)

logger = getLogger(__name__)

NotFoundResponse = HTTPException(status_code=404)
UnExpectedErrorResponse = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
)


class FileAdapter:
    def __init__(self):
        self.client = Minio(
            settings.minio.endpoint,
            access_key=settings.minio.access_key,
            secret_key=settings.minio.secret_key,
            secure=False,
        )

    @staticmethod
    def _get_s3_url(bucket: str, key: str):
        return f"https://api.hackcentrifuge.ru/files/view/{bucket}/{key}"

    async def get_file(self, bucket_name: str, object_name: str):
        return await run_in_threadpool(self._get_file, bucket_name, object_name)

    def _get_file(self, bucket_name: str, object_name: str):
        try:
            res = self.client.get_object(
                bucket_name=bucket_name, object_name=object_name
            )
        except MinioException as e:
            logger.exception("Exception", exc_info=e)
            raise UnExpectedErrorResponse
        if res.status == 200:
            return res.data
        if res.status == 404:
            raise NotFoundResponse
        logger.error(res.reason)
        raise UnExpectedErrorResponse

    def _save_file(
        self,
        upload_file: UploadFile,
        bucket_name: str,
    ) -> str:
        found = self.client.bucket_exists(bucket_name)
        if not found:
            self.client.make_bucket(bucket_name)

        try:
            result = self.client.put_object(
                bucket_name,
                upload_file.filename,
                upload_file.file,
                upload_file.size,
            )
        except Exception as e:
            raise FileDoesntSavedResponse

        return self._get_s3_url(result.bucket_name, result.object_name)

    async def save_file(
        self,
        upload_file: UploadFile,
        bucket_name: str,
    ):
        return await run_in_threadpool(self._save_file, upload_file, bucket_name)


file_adapter = FileAdapter()
