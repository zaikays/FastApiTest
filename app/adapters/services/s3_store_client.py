from typing import NewType, AsyncGenerator, Coroutine

from botocore.config import Config
import boto3
from starlette.concurrency import run_in_threadpool

S3EndpointUrl = NewType("S3EndpointUrl", str)
S3AccessKey = NewType("S3AccessKey", str)
S3SecretKey = NewType("S3SecretKey", str)
S3BucketName = NewType("S3BucketName", str)


class S3Client:

    def __init__(
        self,
        endpoint_url: S3EndpointUrl,
        access_key: S3AccessKey,
        secret_key: S3SecretKey,
        bucket_name: S3BucketName,
    ):
        self.bucket_name = bucket_name

        config = Config(signature_version="s3v4")

        # Create the S3 client instance
        self.client = boto3.client(
            "s3",
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=config,
        )

    async def get_object_async(self, object_name: str) -> Coroutine:
        return await run_in_threadpool(
            self.client.get_object, self.bucket_name, object_name
        )

    def get_object(self, object_name: str):
        return self.client.get_object(Bucket=self.bucket_name, Key=object_name)

    async def upload_file(self, file_object, object_name: str) -> bool:
        try:
            await run_in_threadpool(
                self.client.upload_fileobj, file_object, self.bucket_name, object_name
            )
            return True
        except Exception as e:
            return False

    async def stream_file(
        self, object_name: str, chunk_size: int = 1024 * 1024
    ) -> AsyncGenerator[bytes, None]:
        try:
            response = await run_in_threadpool(
                lambda: self.client.get_object_async(
                    Bucket=self.bucket_name, Key=object_name
                )
            )
            body = response["Body"]

            def reader():
                while True:
                    chunk = body.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

            for chunk in await run_in_threadpool(lambda: list(reader())):
                yield chunk

        except Exception as e:
            return
