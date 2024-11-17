# models.py
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    user_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    google_token: Optional[str] = Field(default=None)
    last_login: datetime = Field(default_factory=datetime.now)    
    is_deleted: bool = Field(default=False)
    creator_id: Optional[UUID] = Field(default=None)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'user'    