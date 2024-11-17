from uuid import UUID
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Opinion(SQLModel, table=True):
    opinion_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    content: str
    answer: Optional[str] = Field(default=None)
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'opinions'
