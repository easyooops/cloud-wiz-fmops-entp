from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class ContactUsCreate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    is_deleted: Optional[bool] = False
    creator_id: Optional[str] = "system"
    created_at: Optional[datetime] = None
    updater_id: Optional[str] = "system"
    updated_at: Optional[datetime] = None

class ContactUsUpdate(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    answer: Optional[str] = None
    is_deleted: Optional[bool] = None
    creator_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updater_id: Optional[str] = None
    updated_at: Optional[datetime] = None

class ContactUsRead(BaseModel):
    contactus_id: int
    customer_name: Optional[str]
    customer_email: Optional[str]
    title: Optional[str]
    content: Optional[str]
    answer: Optional[str]
    is_deleted: bool
    creator_id: Optional[str]
    created_at: datetime
    updater_id: Optional[str]
    updated_at: datetime
