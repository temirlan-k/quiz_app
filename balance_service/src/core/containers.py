from dependency_injector import containers, providers

from src.core.consumer import Consumer
from src.core.db import async_session_factory
from src.core.uow import UnitOfWork
from src.services.balance_service import BalanceService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["src.api.v1"])

    db_session_factory = providers.Object(async_session_factory)

    uow = providers.Factory(UnitOfWork, session_factory=db_session_factory)
    balance_service = providers.Factory(BalanceService, uow=uow)

    consumer = providers.Factory(Consumer, balance_service=balance_service)
