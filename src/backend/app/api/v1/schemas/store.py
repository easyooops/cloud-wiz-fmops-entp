from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID

class StoreBase(BaseModel):
    store_id: Optional[UUID] = None
    credential_id: Optional[UUID] = None
    store_name: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None    
    user_id: Optional[UUID] = None

class FileInfo(BaseModel):
    id: str
    name: str
    size: Optional[int] = None

class StoreWithDirectory(StoreBase):
    provider_logo: Optional[str] = None
    provider_company: Optional[str] = None    
    total_size: Optional[int] = None
    file_count: Optional[int] = None

class StoreWithDirectoryGoogle(StoreBase):
    total_size: Optional[int] = None
    file_count: Optional[int] = None
    files: List[FileInfo] = []


class StoreCreate(BaseModel):
    store_name: str
    description: str
    creator_id: UUID
    updater_id: UUID
    credential_id: UUID
    user_id: UUID

class StoreUpdate(BaseModel):
    store_name: Optional[str] = None
    description: Optional[str] = None
    updater_id: UUID

class Vector(BaseModel):
    user_id: Optional[UUID] = None
    embedding_provider_id: Optional[UUID] = None
    embedding_model_id: Optional[UUID] = None
    storage_provider_id: Optional[UUID] = None
    storage_object_id: Optional[UUID] = None
    vector_db_provider_id: Optional[UUID] = None