from sqlmodel import Session
from typing import Generator, Optional

from app.core.manager import ServiceManager
from app.core.interface.service import ServiceType, StorageService
from app.core.provider.storage.GoogleDrive import GoogleDriveStorageServiceFactory
from app.core.provider.storage.S3 import S3StorageServiceFactory
from app.core.provider.storage.GitHub import GitHubStorageServiceFactory
from app.core.provider.storage.Notion import NotionStorageServiceFactory

# ServiceManager 인스턴스를 생성합니다.
service_manager = ServiceManager()

def get_database(service_type: Optional[ServiceType] = None) -> Generator[Session, None, None]:
    """
    데이터베이스 세션을 생성하고 제공하는 제너레이터 함수입니다.

    Args:
        service_type (Optional[ServiceType]): 사용할 데이터베이스 서비스 타입을 지정합니다.
            지정하지 않으면 기본값으로 MYSQL을 사용합니다.

    Yields:
        Session: 생성된 데이터베이스 세션입니다.
    """

    if service_type is None:
        # 기본 데이터베이스 서비스 타입을 MYSQL로 설정합니다.
        service_type = ServiceType.MYSQL

    # 지정된 서비스 타입의 데이터베이스 서비스를 가져옵니다.
    db_service = service_manager.get_service(service_type)
    # 데이터베이스 세션을 생성합니다.
    db = db_service.get_session()

    try:
        # 생성된 세션을 호출자에게 제공합니다.
        yield db
    finally:
        # 세션 사용이 끝나면 세션을 닫습니다.
        db.close()

def get_storage(service_type: ServiceType, config: dict) -> StorageService:
    storage_service = service_manager.get_service(service_type, config)
    return storage_service
