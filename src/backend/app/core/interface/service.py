from abc import ABC, abstractmethod
from typing import Generator
from enum import Enum

class ServiceType(Enum):
    SQLALCHEMY = "sqlalchemy"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    S3 = "s3"
    GOOGLE_DRIVE = "google_drive"
    NOTION = "notion"
    GITHUB = "github"

class Service(ABC):
    @abstractmethod
    def set_ready(self):
        """
        서비스를 준비 상태로 설정하는 메서드.
        """
        pass

    @abstractmethod
    def teardown(self):
        """
        서비스를 종료하고 리소스를 해제하는 메서드.
        """
        pass

class DatabaseService(Service):
    @abstractmethod
    def get_session(self) -> Generator:
        """
        데이터베이스 세션을 생성하고 제공하는 제너레이터 메서드.
        """
        pass

class StorageService(Service):
    @abstractmethod
    def upload_file(self, file, file_location: str):
        """
        파일을 업로드하는 메서드.
        """
        pass

    @abstractmethod
    def delete_file(self, key: str):
        """
        파일을 삭제하는 메서드.
        """
        pass

    @abstractmethod
    def list_files(self, directory_name: str = ''):
        """
        파일 목록을 반환하는 메서드.
        """
        pass

    @abstractmethod
    def create_directory(self, directory_name: str):
        """
        디렉토리를 생성하는 메서드.
        """
        pass

    @abstractmethod
    def list_all_objects(self, directory_name: str = ''):
        """
        모든 파일 목록을 반환하는 메서드.
        """
        pass

    @abstractmethod
    def delete_directory(self, directory_name: str):
        """
        디렉토리를 삭제하는 메서드.
        """
        pass

    @abstractmethod
    def retry(self, func, retries=5, delay=5, backoff=2):
        """
        재시도 로직을 처리하는 메서드.
        """
        pass

    @abstractmethod
    def get_directory_info(self, directory_name: str = ''):
        """
        디렉토리 정보를 반환하는 메서드.
        """
        pass

    @abstractmethod
    def download_file(self, s3_file_key: str, local_file_path: str):
        """
        디렉토리 정보를 반환하는 메서드.
        """
        pass

class ServiceFactory(ABC):
    @abstractmethod
    def create(self) -> Service:
        """
        새로운 서비스 객체를 생성하는 메서드.
        """
        pass

class NoFactoryRegisteredError(Exception):
    """
    서비스 팩토리가 등록되지 않았을 때 발생하는 예외.
    """
    pass
