
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID, uuid4

class Credential(SQLModel, table=True):
    credential_id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    user_id: UUID = Field(index=True)
    provider_id: UUID = Field(index=True)
    credential_name: str
    access_key: Optional[str] = None
    secret_key: Optional[str] = None
    session_key: Optional[str] = None
    access_token: Optional[str] = None
    api_key: Optional[str] = None
    api_endpoint: Optional[str] = None
    git_clone_url: Optional[str] = None
    git_branch: Optional[str] = None
    git_repo_path: Optional[str] = None
    git_file_filter: Optional[str] = None
    db_user: Optional[str] = None
    db_password: Optional[str] = None
    db_account: Optional[str] = None
    db_role: Optional[str] = None
    db_database: Optional[str] = None
    db_schema: Optional[str] = None
    db_warehouse: Optional[str] = None
    db_query: Optional[str] = None       
    refresh_token: Optional[str] = None
    inner_used: bool = Field(default=False)
    limit_cnt: float = Field(default=0.0)
    is_deleted: bool = Field(default=False)
    creator_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    updater_id: Optional[UUID] = Field(default=None)
    updated_at: datetime = Field(default_factory=datetime.now)

    __tablename__ = 'credentials'
