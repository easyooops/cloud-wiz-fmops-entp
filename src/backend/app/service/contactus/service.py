from typing import Optional
from sqlmodel import Session, desc, select

from app.api.v1.schemas.contactus import ContactUsCreate, ContactUsUpdate
from app.service.contactus.model import ContactUs


class ContactUsService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_contactus(self, title: Optional[str] = None):
        statement = select(ContactUs)
        if title:
            statement = statement.where(ContactUs.title == title)

        statement = statement.order_by(desc(ContactUs.contactus_id))

        return self.session.execute(statement).scalars().all()

    def create_contactus(self, contactus_data: ContactUsCreate):
        try:
            new_contactus = ContactUs(**contactus_data.dict())
            self.session.add(new_contactus)
            self.session.commit()
            self.session.refresh(new_contactus)
            return new_contactus
        except Exception as e:
            raise e
        
    def update_contactus(self, contactus_id: int, contactus_update: ContactUsUpdate):
        try:
            contactus = self.session.get(ContactUs, contactus_id)
            for key, value in contactus_update.dict(exclude_unset=True).items():
                setattr(contactus, key, value)
            self.session.add(contactus)
            self.session.commit()
            self.session.refresh(contactus)
            return contactus
        except Exception as e:
            raise e

    def delete_contactus(self, contactus_id: int):
        try:
            contactus = self.session.get(ContactUs, contactus_id)
            self.session.delete(contactus)
            self.session.commit()
        except Exception as e:
            raise e
