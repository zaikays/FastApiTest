from copy import deepcopy
from typing import AsyncIterator

from dishka import Provider, provide, Scope
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import sessionmaker, Session

from app.adapters.mappers.road_edge_data_mapper import (
    SqlaRoadEdgeDataMapper,
    SqlaRoadEdgeDataMapperAsync,
)
from app.adapters.mappers.road_network_data_mapper import (
    SqlaRoadNetworkDataMapper,
    SqlaRoadNetworkDataMapperAsync,
)
from app.adapters.mappers.road_network_version_data_mapper import (
    SqlaRoadNetworkVersionDataMapper,
    SqlaRoadNetworkVersionDataMapperAsync,
)
from app.adapters.mappers.road_node_data_mapper import (
    SqlaRoadNodeDataMapper,
    SqlaRoadNodeDataMapperAsync,
)
from app.adapters.mappers.user_data_mapper import SqlaUserDataMapperAsync
from app.adapters.services.sqla_flusher import SqlaFlusherAsync, SqlaFlusher
from app.adapters.services.sqla_transaction_manager import (
    SqlaTransactionManagerAsync,
    SqlaTransactionManager,
)
from app.application.common.ports.flusher import FlusherAsync, Flusher
from app.application.common.ports.road_edge_command_gateway import (
    RoadEdgeCommandGatewayAsync,
    RoadEdgeCommandGateway,
)
from app.application.common.ports.road_network_command_gateway import (
    RoadNetworkCommandGateway,
    RoadNetworkCommandGatewayAsync,
)
from app.application.common.ports.road_network_version_command_gateway import (
    RoadNetworkVersionCommandGateway,
    RoadNetworkVersionCommandGatewayAsync,
)
from app.application.common.ports.road_node_command_gateway import (
    RoadNodeCommandGateway,
    RoadNodeCommandGatewayAsync,
)
from app.application.common.ports.transaction_manager import (
    TransactionManagerAsync,
    TransactionManager,
)
from app.application.common.ports.user_command_gateway import UserCommandGatewayAsync
from app.setup.config.settings import AppSettings


class DatabaseProviderAsync(Provider):
    @provide(scope=Scope.APP)
    def get_async_engine_factory(self, settings: AppSettings) -> AsyncEngine:
        return create_async_engine(settings.postgres.dsn)

    @provide(scope=Scope.APP)
    async def get_async_session_factory(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    async def get_async_session(
        self, session_factory: async_sessionmaker[AsyncSession]
    ) -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    road_network_command_gateway_async = provide(
        source=SqlaRoadNetworkDataMapperAsync,
        provides=RoadNetworkCommandGatewayAsync,
        scope=Scope.REQUEST,
    )
    road_network_version_command_gateway_async = provide(
        source=SqlaRoadNetworkVersionDataMapperAsync,
        provides=RoadNetworkVersionCommandGatewayAsync,
        scope=Scope.REQUEST,
    )

    road_node_command_gateway_async = provide(
        source=SqlaRoadNodeDataMapperAsync,
        provides=RoadNodeCommandGatewayAsync,
        scope=Scope.REQUEST,
    )
    road_edge_command_gateway_async = provide(
        source=SqlaRoadEdgeDataMapperAsync,
        provides=RoadEdgeCommandGatewayAsync,
        scope=Scope.REQUEST,
    )
    user_command_gateway = provide(
        source=SqlaUserDataMapperAsync,
        provides=UserCommandGatewayAsync,
        scope=Scope.REQUEST,
    )
    tx_manager_async = provide(
        source=SqlaTransactionManagerAsync,
        provides=TransactionManagerAsync,
        scope=Scope.REQUEST,
    )
    flusher_async = provide(
        source=SqlaFlusherAsync, provides=FlusherAsync, scope=Scope.REQUEST
    )


class DatabaseProvider(Provider):
    """Celery. Just for sync version."""

    @provide(scope=Scope.APP)
    def get_engine_factory(self, settings: AppSettings) -> Engine:
        url = deepcopy(settings.postgres.dsn)
        return create_engine(url.replace("+asyncpg", "+psycopg2"))

    @provide(scope=Scope.APP)
    def get_session_factory(self, engine: Engine) -> sessionmaker[Session]:
        return sessionmaker(bind=engine, class_=Session, expire_on_commit=False)

    @provide(scope=Scope.REQUEST)
    def get_session(self, session_factory: sessionmaker[Session]) -> Session:
        return session_factory()

    road_network_command_gateway = provide(
        source=SqlaRoadNetworkDataMapper,
        provides=RoadNetworkCommandGateway,
        scope=Scope.REQUEST,
    )

    road_network_version_command_gateway = provide(
        source=SqlaRoadNetworkVersionDataMapper,
        provides=RoadNetworkVersionCommandGateway,
        scope=Scope.REQUEST,
    )

    road_edge_command_gateway_async = provide(
        source=SqlaRoadEdgeDataMapper,
        provides=RoadEdgeCommandGateway,
        scope=Scope.REQUEST,
    )

    road_node_command_gateway_async = provide(
        source=SqlaRoadNodeDataMapper,
        provides=RoadNodeCommandGateway,
        scope=Scope.REQUEST,
    )

    tx_manager = provide(
        source=SqlaTransactionManager, provides=TransactionManager, scope=Scope.REQUEST
    )
    flusher = provide(source=SqlaFlusher, provides=Flusher, scope=Scope.REQUEST)
