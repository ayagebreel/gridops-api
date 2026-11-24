from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Fault(Base):
    __tablename__ = "faults"

    id: Mapped[int] = mapped_column(primary_key=True)

    description: Mapped[str] = mapped_column(Text)

    location: Mapped[str] = mapped_column(String(200))

    severity: Mapped[str] = mapped_column(String(20))

    reported_by: Mapped[str] = mapped_column(String(100))

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    work_orders = relationship(
        "WorkOrder",
        back_populates="fault"
    )