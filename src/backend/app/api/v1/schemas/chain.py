from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ChainCreate(BaseModel):
    agent_id: int
    provider_id: int
    connection_order: int
    is_deleted: bool = False
    creator_id: int
    created_at: datetime = datetime.now()
    updater_id: int
    updated_at: datetime = datetime.now()

class ChainUpdate(BaseModel):
    agent_id: Optional[int] = None
    provider_id: Optional[int] = None
    connection_order: Optional[int] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[int] = None
    updated_at: Optional[datetime] = None
