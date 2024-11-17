from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Model(SQLModel, table=True):
    model_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    model_name: str = Field(index=True)
    provider_id: UUID = Field(index=True)
    model_type: str = Field(index=True)  # T, C, I, E
    sort_order: int
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'models'