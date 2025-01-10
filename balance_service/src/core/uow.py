from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import AbstractAsyncContextManager
from src.repositories.balance import BalanceRepository
from src.core.db import async_session_factory


class UnitOfWork(AbstractAsyncContextManager):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory
        self.session: AsyncSession | None = None
        self._registry_repository = {}


    async def __aenter__(self):
        self.session = self._session_factory()
        self.balance_repo = BalanceRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            if exc_type:
                await self.rollback()
            await self.session.close()

    async def commit(self):
        if self.session:
            await self.session.commit()

    async def rollback(self):
        if self.session:
            await self.session.rollback