from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, desc, select
from uuid import UUID

from app.service.agent.model import Agent
from app.api.v1.schemas.agent import AgentCreate, AgentUpdate

class AgentService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_agents(self, agent_id: Optional[UUID] = None, user_id: Optional[UUID] = None):
        statement = select(Agent)
        if agent_id:
            statement = statement.where(Agent.agent_id == agent_id)
        if user_id:
            statement = statement.where(Agent.user_id == user_id)

        statement = statement.order_by(desc(Agent.agent_id))            

        return self.session.execute(statement).scalars().all()

    def create_agent(self, agent_data: AgentCreate):
        try:
            new_agent = Agent(**agent_data.model_dump())
            self.session.add(new_agent)
            self.session.commit()
            self.session.refresh(new_agent)
            return new_agent
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update_agent(self, agent_id: UUID, agent_update: AgentUpdate):
        try:
            agent = self.session.get(Agent, agent_id)
            if not agent:
                raise HTTPException(status_code=404, detail="Agent not found")
            for key, value in agent_update.model_dump(exclude_unset=True).items():
                setattr(agent, key, value)
            self.session.add(agent)
            self.session.commit()
            self.session.refresh(agent)
            return agent
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete_agent(self, agent_id: UUID):
        try:
            agent = self.session.get(Agent, agent_id)
            if not agent:
                raise HTTPException(status_code=404, detail="Agent not found")
            self.session.delete(agent)
            self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


