from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.factories import get_database
from app.service.credential.service import CredentialService
from app.service.credential.model import Credential
from app.api.v1.schemas.credential import CredentialCreate, CredentialProviderJoin, CredentialUpdate
from app.core.exception import internal_server_error
from app.service.auth.service import get_current_user

router = APIRouter()

@router.get("/{credential_id}", response_model=CredentialProviderJoin)
def get_credential_by_id(
    credential_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = CredentialService(session)
        credential = service.get_all_credentials(None, credential_id, None)
        return credential[0]
    except Exception as e:
        raise internal_server_error(e)
    
@router.get("/", response_model=List[CredentialProviderJoin])
def get_credentials(
    user_id: Optional[UUID] = None,
    credential_id: Optional[UUID] = None,
    provider_id: Optional[UUID] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = CredentialService(session)
        return service.get_all_credentials(user_id, credential_id, provider_id)
    except Exception as e:
        raise internal_server_error(e)

@router.post("/", response_model=Credential)
def create_credential(
    credential: CredentialCreate, 
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = CredentialService(session)
        return service.create_credential(credential)
    except Exception as e:
        raise internal_server_error(e)

@router.put("/{credential_id}", response_model=Credential)
def update_credential(
    credential_id: UUID,
    credential_update: CredentialUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = CredentialService(session)
        return service.update_credential(credential_id, credential_update)
    except Exception as e:
        raise internal_server_error(e)

@router.delete("/{credential_id}")
def delete_credential(
    credential_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = CredentialService(session)
        service.delete_credential(credential_id)
        return {"message": "Credential deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)
