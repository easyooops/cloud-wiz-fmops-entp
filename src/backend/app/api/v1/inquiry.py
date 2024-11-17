from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.factories import get_database
from app.core.exception import internal_server_error
from app.service.inquiry.service import InquiryService
from app.service.inquiry.model import Inquiry
from app.api.v1.schemas.inquiry import InquiryCreate, InquiryUpdate
from app.service.auth.service import get_current_user

router = APIRouter()

# GET
@router.get("/", response_model=List[Inquiry])
def get_inquiry(
    inquiry_type: Optional[str] = None,
    title: Optional[str] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = InquiryService(session)
        return service.get_all_inquiries(inquiry_type, title)
    except Exception as e:
        raise internal_server_error(e)

# CREATE    
@router.post("/", response_model=Inquiry)
def create_inquiry(
    inquiry: InquiryCreate, 
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = InquiryService(session)
        return service.create_inquiry(inquiry)
    except Exception as e:
        raise internal_server_error(e)
    
# UPDATE
@router.put("/{inquiry_id}", response_model=Inquiry)
def update_inquiry(
    inquiry_id: int,
    inquiry_update: InquiryUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = InquiryService(session)
        return service.update_inquiry(inquiry_id, inquiry_update)
    except Exception as e:
        raise internal_server_error(e)

# DELETE
@router.delete("/{inquiry_id}")
def delete_inquiry(
    inquiry_id: int,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = InquiryService(session)
        service.delete_inquiry(inquiry_id)
        return {"message": "Inquiry deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)
