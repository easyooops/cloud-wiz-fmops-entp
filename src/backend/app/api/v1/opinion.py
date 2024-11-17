from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.core.factories import get_database
from app.service.opinion.service import OpinionService
from app.api.v1.schemas.opinion import OpinionCreate, OpinionUpdate, OpinionRead
from app.core.exception import internal_server_error
from app.service.auth.service import get_current_user

router = APIRouter()

# GET
@router.get("/", response_model=List[OpinionRead])
def get_opinions(
    title: Optional[str] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = OpinionService(session)
        return service.get_all_opinions(title)
    except Exception as e:
        raise internal_server_error(e)

# CREATE    
@router.post("/", response_model=OpinionRead)
def create_opinion(
    opinion: OpinionCreate, 
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = OpinionService(session)
        return service.create_opinion(opinion)
    except Exception as e:
        raise internal_server_error(e)
    
# UPDATE
@router.put("/{opinion_id}", response_model=OpinionRead)
def update_opinion(
    opinion_id: int,
    opinion_update: OpinionUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = OpinionService(session)
        return service.update_opinion(opinion_id, opinion_update)
    except Exception as e:
        raise internal_server_error(e)

# DELETE
@router.delete("/{opinion_id}")
def delete_opinion(
    opinion_id: int,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = OpinionService(session)
        service.delete_opinion(opinion_id)
        return {"message": "Opinion deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)
