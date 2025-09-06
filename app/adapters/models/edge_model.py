

from geoalchemy2 import Geometry
from sqlalchemy import ForeignKey, JSON, Index, TypeDecorator
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.models.base import Base
from app.adapters.models.helpers.jsonb_decimal import JSONBWithDecimal


class RoadEdgeModel(Base):
    __tablename__ = "road_edges"
    __table_args__ = (
        Index("idx_fast_road_edges_geometry", "geometry", postgresql_using="gist"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    version_id: Mapped[int] = mapped_column(
        ForeignKey(
            "road_network_versions.id",
            name="fk_road_edges_version_id",
            ondelete="CASCADE",
        )
    )
    start_node_id: Mapped[int] = mapped_column(
        ForeignKey("road_nodes.id", name="fk_road_edges_start_node_id")
    )
    end_node_id: Mapped[int] = mapped_column(
        ForeignKey("road_nodes.id", name="fk_road_edges_end_node_id")
    )

    properties: Mapped[dict] = mapped_column(JSONBWithDecimal, nullable=False)
    geometry: Mapped[str] = mapped_column(
        Geometry("LINESTRING", srid=4326), nullable=False
    )

    version: Mapped["RoadNetworkVersionModel"] = relationship(
        back_populates="road_edges"
    )

    start_node: Mapped["RoadNodeModel"] = relationship(
        foreign_keys=[start_node_id],
        backref="outgoing_edges",
    )
    end_node: Mapped["RoadNodeModel"] = relationship(
        foreign_keys=[end_node_id],
        backref="incoming_edges",
    )
