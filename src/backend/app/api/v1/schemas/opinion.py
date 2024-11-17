from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class OpinionCreate(BaseModel):
    title: str
    content: str
    answer: Optional[str] = None
    is_deleted: bool = False
    creator_id: UUID
    created_at: datetime = datetime.now()
    updater_id: UUID
    updated_at: datetime = datetime.now()

class OpinionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None

class OpinionRead(BaseModel):
    opinion_id: int
    title: str
    content: str
    answer: Optional[str]
    is_deleted: bool
    creator_id: UUID
    created_at: datetime
    updater_id: Optional[UUID]
    updated_at: datetime
