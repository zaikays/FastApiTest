from abc import abstractmethod
from typing import Protocol


class FlusherAsync(Protocol):

    @abstractmethod
    async def flush(self) -> None:
        pass


class Flusher(Protocol):

    @abstractmethod
    def flush(self) -> None:
        pass
