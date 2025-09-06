from abc import abstractmethod
from typing import Protocol, AsyncGenerator


class FileManager(Protocol):

    @abstractmethod
    def validate_file_extension(
        self, filename: str, allowed_extensions: list[str]
    ) -> None: ...

    @abstractmethod
    def validate_file_size(self, file, max_size: int) -> None: ...

    @abstractmethod
    async def upload_file(self, file, object_name: str) -> str | None: ...

    @abstractmethod
    def stream_file(
        self, object_name: str, chunk_size: int
    ) -> AsyncGenerator[bytes, None]: ...
