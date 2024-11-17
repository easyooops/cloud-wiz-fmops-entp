from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Chain(SQLModel, table=True):
    chain_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    agent_id: int
    provider_id: int
    connection_order: int
    is_deleted: bool = Field(default=False)
    creator_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    updater_id: Optional[int] = Field(default=None)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'chain' 
