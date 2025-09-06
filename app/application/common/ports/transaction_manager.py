from abc import abstractmethod
from typing import Protocol


class TransactionManagerAsync(Protocol):

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class TransactionManager(Protocol):

    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def rollback(self) -> None: ...
