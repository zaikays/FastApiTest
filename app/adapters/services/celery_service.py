from typing import NewType

import ijson
from celery import Celery
from typing import Any

from dishka import make_container, FromDishka
from dishka.integrations.celery import DishkaTask, setup_dishka
from shapely.geometry import LineString

from app.adapters.models import RoadEdgeModel
from app.application.common.ports.road_edge_command_gateway import (
    RoadEdgeCommandGateway,
)
from app.application.common.ports.road_node_command_gateway import (
    RoadNodeCommandGateway,
)
from app.setup.config.settings import AppSettings, load_settings

CeleryBrokerUrl = NewType("CeleryBrokerUrl", str)
CeleryResultBackend = NewType("CeleryResultBackend", str)


class CeleryService:
    def __init__(
        self,
        broker_url: str = "redis://localhost:6379/0",
        backend_url: str = "redis://localhost:6379/1",
    ):
        from app.setup.ioc.settings import SettingsProvider
        from app.setup.ioc.database import DatabaseProvider
        from app.setup.ioc.database import DatabaseProviderAsync
        from app.setup.ioc.application import ApplicationProvider

        self._app_celery = Celery(
            "my_app", broker=broker_url, backend=backend_url, task_cls=DishkaTask
        )
        loaded_settings = load_settings()
        container = make_container(
            *(
                SettingsProvider(),
                DatabaseProvider(),
                DatabaseProviderAsync(),
                ApplicationProvider(),
            ),
            context={AppSettings: loaded_settings},
        )
        setup_dishka(container=container, app=self._app_celery)
        self._register_tasks()

    @property
    def app(self):
        return self._app_celery

    def _register_tasks(self):
        from app.adapters.services.s3_store_client import S3Client
        from app.application.common.ports.road_network_version_command_gateway import (
            RoadNetworkVersionCommandGateway,
        )
        from app.application.common.ports.transaction_manager import TransactionManager
        from app.application.common.ports.flusher import Flusher

        @self.app.task(name="parse_geojson")
        def parse_geojson(
            road_network_version_id: int,
            s3: FromDishka[S3Client] = None,
            road_network_version_command_gateway: FromDishka[
                RoadNetworkVersionCommandGateway
            ] = None,
            road_node_command_gateway: FromDishka[RoadNodeCommandGateway] = None,
            road_edge_command_gateway: FromDishka[RoadEdgeCommandGateway] = None,
            flusher: FromDishka[Flusher] = None,
            transaction_manager: FromDishka[TransactionManager] = None,
        ):
            network_version = road_network_version_command_gateway.read_by_id(
                road_network_version_id, for_update=True
            )
            if not network_version:
                return None
            response = s3.get_object(network_version.file_name)
            file_obj = response["Body"]
            from geoalchemy2.shape import from_shape

            for feature in ijson.items(file_obj, "features.item"):
                start_node_id = None
                end_node_id = None
                cords = feature["geometry"]["coordinates"]
                for point in feature["geometry"]["coordinates"]:
                    road_node = road_node_command_gateway.insert(
                        network_version.network_id, point, True
                    )
                    start_node_id = (
                        road_node.id if start_node_id is None else start_node_id
                    )
                    end_node_id = road_node.id if road_node else end_node_id

                line = LineString(cords)

                geometry = from_shape(line, srid=4326)
                road_edge_command_gateway.add(
                    RoadEdgeModel(
                        start_node_id=start_node_id,
                        end_node_id=end_node_id,
                        properties=feature["properties"],
                        geometry=geometry,
                        version_id=network_version.id,
                    )
                )
                flusher.flush()
                transaction_manager.commit()
            return road_network_version_id

    def _call_task_async(self, task_name: str, *args, **kwargs) -> Any:
        return self._app_celery.send_task(task_name, args=args, kwargs=kwargs)

    def parse_geojson(self, road_network_version_id: int):
        return self._call_task_async("parse_geojson", road_network_version_id)
