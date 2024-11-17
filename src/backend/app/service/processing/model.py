from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Processing(SQLModel, table=True):
    processing_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    processing_type: str
    processing_name: str
    processing_desc: Optional[str] = None
    template: Optional[str] = None
    pii_masking: Optional[str] = None
    normalization: Optional[str] = None
    stopword_removal: Optional[str] = None
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)

    __tablename__ = 'processing'