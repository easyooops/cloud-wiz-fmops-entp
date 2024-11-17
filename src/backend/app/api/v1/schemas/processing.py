from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ProcessingCreate(BaseModel):
    user_id: UUID
    processing_type: str
    processing_name: str
    processing_desc: Optional[str] = None    
    template: Optional[str] = None
    pii_masking: Optional[str] = None
    normalization: Optional[str] = None
    stopword_removal: Optional[str] = None
    is_deleted: bool = False
    creator_id: UUID
    created_at: datetime = datetime.now()
    updater_id: Optional[UUID] = None
    updated_at: datetime = datetime.now()

class ProcessingUpdate(BaseModel):
    user_id: Optional[UUID] = None
    processing_type: Optional[str] = None
    processing_name: str
    processing_desc: Optional[str] = None    
    template: Optional[str] = None
    pii_masking: Optional[str] = None
    normalization: Optional[str] = None
    stopword_removal: Optional[str] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None
