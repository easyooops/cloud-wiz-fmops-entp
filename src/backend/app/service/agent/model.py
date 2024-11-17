from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Agent(SQLModel, table=True):
    agent_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    agent_name: str
    agent_description: Optional[str] = None
    fm_provider_type: str
    fm_provider_id: UUID = Field(index=True)
    fm_model_id: UUID = Field(index=True)
    fm_temperature: float = Field(default=0.7)
    fm_top_p: float = Field(default=0.9)
    fm_request_token_limit: int = Field(default=5000)
    fm_response_token_limit: int = Field(default=5000)
    embedding_enabled: bool = Field(default=False)
    embedding_provider_id: Optional[UUID] = None
    embedding_model_id: Optional[UUID] = None
    storage_provider_id: Optional[UUID] = None
    storage_object_id: Optional[UUID] = None
    vector_db_provider_id: Optional[UUID] = None
    processing_enabled: bool = Field(default=False)
    pre_processing_id: Optional[UUID] = None
    post_processing_id: Optional[UUID] = None
    template_enabled: bool = Field(default=False)
    template: Optional[str] = None
    expected_request_count: int = Field(default=0)
    expected_token_count: int = Field(default=0)
    expected_cost: float = Field(default=0.0)
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)

    __tablename__ = 'agents'
