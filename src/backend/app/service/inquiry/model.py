from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Inquiry model
class Inquiry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    inquiry_type: str = Field(index=True)
    title: str = Field(index=True)
    content: str = Field(index=True)
    response_content: Optional[str] = Field(default=None)
    processing_type: str
    creator_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    updater_id: Optional[int] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'inquiry'