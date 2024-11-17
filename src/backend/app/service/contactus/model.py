from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class ContactUs(SQLModel, table=True):
    contactus_id: Optional[int] = Field(default=None, primary_key=True, index=True)
    customer_name: Optional[str] = Field(default=None)
    customer_email: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    content: Optional[str] = Field(default=None)
    answer: Optional[str] = Field(default=None)
    is_deleted: Optional[bool] = Field(default=False)
    creator_id: Optional[str] = Field(default="system")
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updater_id: Optional[str] = Field(default="system")
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)

    __tablename__ = 'contactus'
