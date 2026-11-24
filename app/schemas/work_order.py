from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


Status = Literal[
    "open",
    "assigned",
    "in_progress",
    "closed",
    "cancelled"
]


class WorkOrderCreate(BaseModel):
    fault_id: int
    assigned_to: str | None = None


class StatusUpdate(BaseModel):
    status: Status


class WorkOrderResponse(BaseModel):
    id: int
    fault_id: int
    assigned_to: str | None
    status: Status
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PartCreate(BaseModel):
    component_id: int
    quantity: int = Field(ge=1, le=100)