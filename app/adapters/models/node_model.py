from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, Index, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.models.base import Base


class RoadNodeModel(Base):
    __tablename__ = "road_nodes"
    __table_args__ = (
        Index("idx_fast_road_nodes_geometry", "geometry", postgresql_using="gist"),
        UniqueConstraint(
            "network_id",
            func.ST_AsBinary("geometry").label("geometry"),
            name="uq_road_nodes_network_geometry",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    network_id: Mapped[int] = mapped_column(
        ForeignKey(
            "road_networks.id", name="fk_road_nodes_network_id", ondelete="CASCADE"
        )
    )
    geometry: Mapped[Geometry] = mapped_column(
        Geometry(geometry_type="POINT", srid=4326), nullable=False
    )

    network: Mapped["RoadNetworkModel"] = relationship(back_populates="nodes")
