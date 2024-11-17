from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.factories import get_database

from app.service.chain.model import Chain
from app.service.chain.service import ChainService
from app.api.v1.schemas.chain import ChainCreate, ChainUpdate
from app.core.exception import internal_server_error
from app.service.auth.service import get_current_user

router = APIRouter()

# GET
@router.get("/", response_model=List[Chain])
def get_chains(
    provider_id: Optional[int] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ChainService(session)
        return service.get_all_chains(provider_id)
    except Exception as e:
        raise internal_server_error(e)

# CREATE    
@router.post("/", response_model=Chain)
def create_chain(
    chain: ChainCreate, 
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = ChainService(session)
        return service.create_chain(chain)
    except Exception as e:
        raise internal_server_error(e)
    
# UPDATE
@router.put("/{chain_id}", response_model=Chain)
def update_chain(
    chain_id: int,
    chain_update: ChainUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = ChainService(session)
        return service.update_chain(chain_id, chain_update)
    except Exception as e:
        raise internal_server_error(e)

# DELETE
@router.delete("/{chain_id}")
def delete_chain(
    chain_id: int,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ChainService(session)
        service.delete_chain(chain_id)
        return {"message": "Chain deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)