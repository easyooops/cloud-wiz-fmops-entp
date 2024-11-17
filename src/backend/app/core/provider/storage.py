from abc import abstractmethod
from app.core.interface.service import Service

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