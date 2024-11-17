from typing import Optional
from pydantic import BaseModel
from uuid import UUID

class ModelCreate(BaseModel):
    model_name: str
    provider_id: UUID
    model_type: str
    sort_order: int
    creator_id: UUID
    updater_id: Optional[UUID] = None

class ModelUpdate(BaseModel):
    model_type: Optional[str] = None
    sort_order: Optional[int] = None
    updater_id: Optional[UUID] = None
