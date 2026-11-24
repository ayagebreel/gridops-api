from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String

from app.database import Base


class Component(Base):
    __tablename__ = "components"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )

    code: Mapped[str] = mapped_column(
        String(50),
        unique=True
    )

    unit: Mapped[str] = mapped_column(String(30))

    parts = relationship(
        "WorkOrderPart",
        back_populates="component"
    )


class WorkOrderPart(Base):
    __tablename__ = "work_order_parts"

    id: Mapped[int] = mapped_column(primary_key=True)

    work_order_id: Mapped[int] = mapped_column(
        ForeignKey("work_orders.id")
    )

    component_id: Mapped[int] = mapped_column(
        ForeignKey("components.id")
    )

    quantity: Mapped[int] = mapped_column(nullable=False)

    work_order = relationship(
        "WorkOrder",
        back_populates="parts"
    )

    component = relationship(
        "Component",
        back_populates="parts"
    )