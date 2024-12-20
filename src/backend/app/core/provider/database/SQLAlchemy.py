import os
from loguru import logger

from sqlmodel import Session, create_engine

from app.core.interface.service import Service, ServiceFactory

class SQLAlchemyService(Service):
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})

    def get_session(self) -> Session:
        return Session(bind=self.engine)

    def set_ready(self):
        logger.info("SQLModelService is ready")

    def teardown(self):
        logger.info("SQLModelService is being torn down")
        self.engine.dispose()

class SQLAlchemyServiceFactory(ServiceFactory):
    def create(self) -> SQLAlchemyService:
        return SQLAlchemyService(os.getenv("SQLALCHEMY_DATABASE_URL"))
