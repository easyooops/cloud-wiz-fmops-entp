from typing import Optional
from uuid import UUID
from sqlmodel import Session, desc, select

from app.api.v1.schemas.opinion import OpinionCreate, OpinionUpdate
from app.service.opinion.model import Opinion

class OpinionService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_opinions(self, title: Optional[str] = None):
        statement = select(Opinion)
        if title:
            statement = statement.where(Opinion.title == title)

        statement = statement.order_by(desc(Opinion.opinion_id))

        return self.session.execute(statement).scalars().all()

    def create_opinion(self, opinion_data: OpinionCreate):
        try:
            new_opinion = Opinion(**opinion_data.dict())
            self.session.add(new_opinion)
            self.session.commit()
            self.session.refresh(new_opinion)
            return new_opinion
        except Exception as e:
            raise e
        
    def update_opinion(self, opinion_id: int, opinion_update: OpinionUpdate):
        try:
            opinion = self.session.get(Opinion, opinion_id)
            for key, value in opinion_update.dict(exclude_unset=True).items():
                setattr(opinion, key, value)
            self.session.add(opinion)
            self.session.commit()
            self.session.refresh(opinion)
            return opinion
        except Exception as e:
            raise e

    def delete_opinion(self, opinion_id: int):
        try:
            opinion = self.session.get(Opinion, opinion_id)
            self.session.delete(opinion)
            self.session.commit()
        except Exception as e:
            raise e
