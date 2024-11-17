from typing import List, Optional
from fastapi import HTTPException
from sqlmodel import Session, select

from app.service.chain.model import Chain
from app.api.v1.schemas.chain import ChainCreate, ChainUpdate

class ChainService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_chains(self, provider_id: Optional[int] = None):
        statement = select(Chain)
        if provider_id:
            statement = statement.where(Chain.provider_id == provider_id)
        return self.session.execute(statement).scalars().all()

    def create_chain(self, chain_data: ChainCreate):
        try:
            new_chain = Chain(**chain_data.model_dump())
            self.session.add(new_chain)
            self.session.commit()
            self.session.refresh(new_chain)
            return new_chain
        except Exception as e:
            raise e
        
    def update_chain(self, chain_id: int, chain_update: ChainUpdate):
        try:
            chain = self.session.get(Chain, chain_id)
            if not chain:
                raise HTTPException(status_code=404, detail="Chain not found")
            for key, value in chain_update.model_dump().items():
                setattr(chain, key, value)
            self.session.add(chain)
            self.session.commit()
            self.session.refresh(chain)
            return chain
        except Exception as e:
            raise e

    def delete_chain(self, chain_id: int):
        try:
            chain = self.session.get(Chain, chain_id)
            if not chain:
                raise HTTPException(status_code=404, detail="Chain not found")
            self.session.delete(chain)
            self.session.commit()
        except Exception as e:
            raise e
