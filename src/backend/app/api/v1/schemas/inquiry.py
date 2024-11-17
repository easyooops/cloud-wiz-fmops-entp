from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# Inquiry schema for creation
class InquiryCreate(BaseModel):
    inquiry_type: str
    title: str
    content: str
    response_content: Optional[str] = None
    processing_type: str
    creator_id: int
    created_at: datetime = datetime.now()
    updater_id: Optional[int] = None
    updated_at: datetime = datetime.now()

# Inquiry schema for update
class InquiryUpdate(BaseModel):
    inquiry_type: Optional[str]
    title: Optional[str]
    content: Optional[str]
    response_content: Optional[str]
    processing_type: Optional[str]
    updater_id: Optional[int] = None
    updated_at: datetime = datetime.now()
