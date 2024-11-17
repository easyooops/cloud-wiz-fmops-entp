from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Provider(SQLModel, table=True):
    provider_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    name: str = Field(index=True)
    company: str = Field(index=True)
    pvd_key: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None, index=True)
    logo: Optional[str] = Field(default=None)
    type: str
    sort_order: int
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'providers' 