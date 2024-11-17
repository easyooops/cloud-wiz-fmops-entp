from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProviderCreate(BaseModel):
    company: str
    name: str
    description: str
    pvd_key: str
    logo: str
    type: str
    sort_order: int
    is_deleted: bool = False
    creator_id: UUID
    created_at: datetime = datetime.now()
    updater_id: UUID
    updated_at: datetime = datetime.now()

class ProviderUpdate(BaseModel):
    company: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    pvd_key: Optional[str] = None
    logo: Optional[str] = None
    type: Optional[str] = None
    sort_order: Optional[int] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None    