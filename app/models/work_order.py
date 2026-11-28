from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    fault_id: Mapped[int] = mapped_column(
        ForeignKey("faults.id"),
        nullable=False
    )

    assigned_to: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="open"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    fault = relationship(
        "Fault",
        back_populates="work_orders"
    )

    parts = relationship(
        "WorkOrderPart",
        back_populates="work_order",
        cascade="all, delete-orphan"
    )