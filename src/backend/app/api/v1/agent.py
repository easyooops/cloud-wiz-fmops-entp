from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app.core.interface.service import ServiceType
from app.core.factories import get_database
from app.service.agent.service import AgentService
from app.api.v1.schemas.agent import AgentCreate, AgentUpdate
from app.core.exception import internal_server_error
from app.service.agent.model import Agent
from app.api.v1.schemas.chat import ChatResponse
from app.service.prompt.service import PromptService
from app.service.auth.service import get_current_user

router = APIRouter()

@router.get("/prompt/{agent_id}", response_model=ChatResponse)
def get_agents_prompt(
    agent_id: UUID,    
    query: Optional[str] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)    
):
    try:
        service = PromptService(session)
        # answer = service.get_prompt(agent_id, query)
        # tokens = service._get_token_counts(agent_id, answer)
        # return ChatResponse(answer=answer, tokens=tokens)
        return service.get_prompt(agent_id, query)
    except Exception as e:
        raise internal_server_error(e)
    
@router.get("/{agent_id}", response_model=Agent)
def get_agents_by_id(
    agent_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = AgentService(session)
        agents: List[Agent] = service.get_all_agents(agent_id, None)
        
        if not agents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent with ID {agent_id} not found"
            )
        
        return agents[0]
    except Exception as e:
        raise internal_server_error(e)
    
@router.get("/", response_model=List[Agent])
def get_agents(
    agent_id: Optional[UUID] = None,
    user_id: Optional[UUID] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = AgentService(session)
        return service.get_all_agents(agent_id, user_id)
    except Exception as e:
        raise internal_server_error(e)

@router.post("/", response_model=Agent)
def create_agent(
    agent: AgentCreate, 
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = AgentService(session)
        return service.create_agent(agent)
    except Exception as e:
        raise internal_server_error(e)

@router.put("/{agent_id}", response_model=Agent)
def update_agent(
    agent_id: UUID,
    agent_update: AgentUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = AgentService(session)
        return service.update_agent(agent_id, agent_update)
    except Exception as e:
        raise internal_server_error(e)

@router.delete("/{agent_id}")
def delete_agent(
    agent_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        service = AgentService(session)
        service.delete_agent(agent_id)
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)
