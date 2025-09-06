from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.adapters.models.base import Base


class RoadNetworkModel(Base):
    __tablename__ = "road_networks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_road_networks_customer_id", ondelete="CASCADE")
    )
    created_at: Mapped[datetime] = mapped_column(default=func.now())

    versions: Mapped[list["RoadNetworkVersionModel"]] = relationship(
        back_populates="network", cascade="all, delete-orphan"
    )
    nodes: Mapped[list["RoadNodeModel"]] = relationship(
        back_populates="network", cascade="all, delete-orphan"
    )
