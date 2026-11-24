from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class FaultCreate(BaseModel):
    description: str = Field(min_length=5, max_length=1000)
    location: str = Field(min_length=2, max_length=200)
    severity: str = Field(pattern="^(low|medium|high|critical)$")
    reported_by: str = Field(min_length=2, max_length=100)


class FaultResponse(BaseModel):
    id: int
    description: str
    location: str
    severity: str
    reported_by: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)