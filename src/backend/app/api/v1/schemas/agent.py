from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, field_validator

class AgentCreate(BaseModel):
    user_id: UUID
    agent_name: str
    agent_description: Optional[str] = None
    fm_provider_type: str
    fm_provider_id: UUID
    fm_model_id: UUID
    fm_temperature: float = 0.7
    fm_top_p: float = 0.9
    fm_request_token_limit: int = 5000
    fm_response_token_limit: int = 5000
    embedding_enabled: bool = False
    embedding_provider_id: Optional[UUID] = None
    embedding_model_id: Optional[UUID] = None
    storage_provider_id: Optional[UUID] = None
    storage_object_id: Optional[UUID] = None
    vector_db_provider_id: Optional[UUID] = None
    processing_enabled: bool = False
    pre_processing_id: Optional[UUID] = None
    post_processing_id: Optional[UUID] = None
    template_enabled: bool = False
    template: Optional[str] = None
    expected_request_count: int = 0
    expected_token_count: int = 0
    expected_cost: float = 0.0
    is_deleted: bool = False
    creator_id: UUID
    created_at: datetime = datetime.now()
    updater_id: Optional[UUID] = None
    updated_at: datetime = datetime.now()

    @field_validator('embedding_provider_id', 'embedding_model_id', 'storage_provider_id', 
               'storage_object_id', 'vector_db_provider_id', 'pre_processing_id', 
               'post_processing_id', mode='before')
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v
    
class AgentUpdate(BaseModel):
    user_id: Optional[UUID] = None
    agent_name: Optional[str] = None
    agent_description: Optional[str] = None
    fm_provider_type: Optional[str] = None
    fm_provider_id: Optional[UUID] = None
    fm_model_id: Optional[UUID] = None
    fm_temperature: Optional[float] = None
    fm_top_p: Optional[float] = None
    fm_request_token_limit: Optional[int] = None
    fm_response_token_limit: Optional[int] = None
    embedding_enabled: Optional[bool] = None
    embedding_provider_id: Optional[UUID] = None
    embedding_model_id: Optional[UUID] = None
    storage_provider_id: Optional[UUID] = None
    storage_object_id: Optional[UUID] = None
    vector_db_provider_id: Optional[UUID] = None
    processing_enabled: Optional[bool] = None
    pre_processing_id: Optional[UUID] = None
    post_processing_id: Optional[UUID] = None
    template_enabled: bool = False
    template: Optional[str] = None    
    expected_request_count: Optional[int] = None
    expected_token_count: Optional[int] = None
    expected_cost: Optional[float] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[UUID] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[UUID] = None
    updated_at: Optional[datetime] = None

    @field_validator('embedding_provider_id', 'embedding_model_id', 'storage_provider_id', 
               'storage_object_id', 'vector_db_provider_id', 'pre_processing_id', 
               'post_processing_id', mode='before')
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v