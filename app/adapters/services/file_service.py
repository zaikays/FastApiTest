import time
from typing import AsyncGenerator

from app.adapters.services.s3_store_client import S3Client
from app.domain.exceptions.base import DomainFieldError
from app.domain.services.file_manager import FileManager


class FileService(FileManager):
    def __init__(self, s3_client: S3Client):
        self._s3_client = s3_client

    def validate_file_extension(self, filename: str, allowed_extensions: list[str]):
        ext = filename.lower().rsplit(".", 1)[-1]
        if f".{ext}" not in allowed_extensions:
            raise DomainFieldError(
                f"File extension '{ext}' is not allowed. Allowed: {allowed_extensions}"
            )

    def validate_file_size(self, file, max_size: int):
        if file.file.size > max_size:
            raise DomainFieldError(f"File size exceeds {max_size} bytes.")

    async def upload_file(self, file, object_name: str) -> str | None:
        timestamp = int(time.time() * 1000)
        object_name_with_timestamp = f"{timestamp}_{object_name}"
        try:
            await self._s3_client.upload_file(file, object_name_with_timestamp)
        except Exception as e:
            pass
        else:
            return object_name_with_timestamp

    def stream_file(
        self, object_name: str, chunk_size: int
    ) -> AsyncGenerator[bytes, None]:
        return self._s3_client.stream_file(object_name, chunk_size=chunk_size)
