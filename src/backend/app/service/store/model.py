from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Store(SQLModel, table=True):
    store_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    credential_id: UUID = Field(index=True)
    store_name: str
    description: Optional[str] = None
    is_deleted: bool = False
    creator_id: UUID
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)