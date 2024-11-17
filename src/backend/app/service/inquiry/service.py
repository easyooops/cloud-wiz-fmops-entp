from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select

from app.service.inquiry.model import Inquiry
from app.api.v1.schemas.inquiry import InquiryCreate, InquiryUpdate

class InquiryService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_inquiries(self, inquiry_type: Optional[str] = None, title: Optional[str] = None):
        statement = select(Inquiry)
        if inquiry_type:
            statement = statement.where(Inquiry.inquiry_type == inquiry_type)
        if title:
            statement = statement.where(Inquiry.title == title)
        return self.session.execute(statement).scalars().all()

    def create_inquiry(self, inquiry_data: InquiryCreate):
        try:
            new_inquiry = Inquiry(**inquiry_data.model_dump())
            self.session.add(new_inquiry)
            self.session.commit()
            self.session.refresh(new_inquiry)
            return new_inquiry
        except Exception as e:
            raise e
        
    def update_inquiry(self, inquiry_id: int, inquiry_update: InquiryUpdate):
        try:
            inquiry = self.session.get(Inquiry, inquiry_id)
            if not inquiry:
                raise HTTPException(status_code=404, detail="Inquiry not found")
            for key, value in inquiry_update.dict().items():
                setattr(inquiry, key, value)
            self.session.add(inquiry)
            self.session.commit()
            self.session.refresh(inquiry)
            return inquiry
        except Exception as e:
            raise e

    def delete_inquiry(self, inquiry_id: int):
        try:
            inquiry = self.session.get(Inquiry, inquiry_id)
            if not inquiry:
                raise HTTPException(status_code=404, detail="Inquiry not found")
            self.session.delete(inquiry)
            self.session.commit()
        except Exception as e:
            raise e
