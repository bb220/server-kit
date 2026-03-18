from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class CustomerCreate(BaseModel):
    name: str
    city: str
    state: str


class CustomerUpdate(BaseModel):
    name: str | None = None
    city: str | None = None
    state: str | None = None


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    city: str
    state: str
    created_at: datetime
    updated_at: datetime


class CustomerListResponse(BaseModel):
    data: list[CustomerRead]
