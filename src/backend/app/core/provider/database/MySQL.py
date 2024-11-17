import os
from loguru import logger

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from app.core.interface.service import Service, ServiceFactory
from app.service.auth.service import AuthService

class MySQLService(Service):
    def __init__(self, db_url: str):
        self.engine = create_engine(
            db_url, 
            pool_pre_ping=True,     # 커넥션 풀에서 커넥션을 사용하기 전에 ping을 수행하여 커넥션이 유효한지 확인합니다.
            pool_size=10,           # 최소 연결 수
            max_overflow=5,         # 최대 추가 연결 수 (pool_size 초과)
            pool_timeout=30,        # 연결 대기 시간 (초)
            pool_recycle=3600,      # 연결 재사용 주기 (초)            
            echo=True               # SQLAlchemy가 실행하는 모든 SQL 쿼리를 로그에 출력
        )
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Session = SessionLocal
        Base = declarative_base()

    def get_session(self) -> sessionmaker:
        return self.Session()

    def set_ready(self):
        logger.info("MySQL is ready")

    def teardown(self):
        self.engine.dispose()

class MySQLServiceFactory(ServiceFactory):
    def create(self) -> MySQLService:
        return MySQLService(AuthService.get_db_info())