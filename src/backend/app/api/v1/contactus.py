from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.factories import get_database
from app.service.contactus.service import ContactUsService
from app.api.v1.schemas.contactus import ContactUsCreate, ContactUsUpdate, ContactUsRead
from app.core.exception import internal_server_error
from app.service.auth.service import get_current_user

router = APIRouter()

# GET
@router.get("/", response_model=List[ContactUsRead])
def get_contactus(
    title: Optional[str] = None,
    session: Session = Depends(get_database)
):
    try:
        service = ContactUsService(session)
        return service.get_all_contactus(title)
    except Exception as e:
        raise internal_server_error(e)

# CREATE    
@router.post("/", response_model=ContactUsRead)
def create_contactus(
    contactus: ContactUsCreate, 
    session: Session = Depends(get_database)
):
    try:
        service = ContactUsService(session)
        return service.create_contactus(contactus)
    except Exception as e:
        raise internal_server_error(e)
    
# UPDATE
@router.put("/{contactus_id}", response_model=ContactUsRead)
def update_contactus(
    contactus_id: int,
    contactus_update: ContactUsUpdate,
    session: Session = Depends(get_database)
):
    try:
        service = ContactUsService(session)
        return service.update_contactus(contactus_id, contactus_update)
    except Exception as e:
        raise internal_server_error(e)

# DELETE
@router.delete("/{contactus_id}")
def delete_contactus(
    contactus_id: int,
    session: Session = Depends(get_database)
):
    try:
        service = ContactUsService(session)
        service.delete_contactus(contactus_id)
        return {"message": "ContactUs deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)
