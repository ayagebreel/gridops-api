from pydantic import BaseModel, ConfigDict, Field


class ComponentCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    code: str = Field(min_length=2, max_length=50)
    unit: str = Field(min_length=1, max_length=30)


class ComponentResponse(BaseModel):
    id: int
    name: str
    code: str
    unit: str

    model_config = ConfigDict(from_attributes=True)