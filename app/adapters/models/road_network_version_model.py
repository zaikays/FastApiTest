from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.adapters.models.base import Base


class RoadNetworkVersionModel(Base):
    __tablename__ = "road_network_versions"

    id: Mapped[int] = mapped_column(primary_key=True)
    network_id: Mapped[int] = mapped_column(
        ForeignKey(
            "road_networks.id", name="fk_versions_network_id", ondelete="CASCADE"
        )
    )
    version_number: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    file_name: Mapped[str] = mapped_column(nullable=True)

    network: Mapped["RoadNetworkModel"] = relationship(back_populates="versions")
    road_edges: Mapped[list["RoadEdgeModel"]] = relationship(
        back_populates="version", cascade="all, delete-orphan"
    )
