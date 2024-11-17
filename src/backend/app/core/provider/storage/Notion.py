from notion_client import Client
from app.core.interface.service import ServiceFactory, StorageService

class NotionStorageService(StorageService):
    def __init__(self, api_token: str, database_id: str):
        self.api_token = api_token
        self.database_id = database_id
        self.client = Client(auth=self.api_token)

    def upload_file(self, file, file_location: str):
        # Notion API에서는 파일 업로드 기능이 제한적입니다. 파일을 노트에 첨부하거나 특정 블록에 파일 링크를 추가할 수 있습니다.
        response = self.client.pages.create(
            parent={"database_id": self.database_id},
            properties={
                "title": [{"text": {"content": file_location}}],
                "file": [{"type": "external", "external": {"url": file}}]
            }
        )
        print(f"File uploaded: {response}")

    def delete_file(self, key: str):
        # Notion API에서는 파일 삭제가 제한적입니다. 대신 페이지를 아카이브 처리할 수 있습니다.
        response = self.client.blocks.delete(block_id=key)
        print(f"File deleted: {response}")

    def list_files(self, directory_name: str = ''):
        # Notion API에서는 파일 목록 조회 기능이 제한적입니다. 대신 페이지 목록을 조회할 수 있습니다.
        response = self.client.databases.query(database_id=self.database_id)
        return response.get('results', [])

    def create_directory(self, directory_name: str):
        # Notion API에서는 디렉토리 생성 기능이 없습니다. 대신 데이터베이스나 페이지를 생성할 수 있습니다.
        response = self.client.databases.create(
            parent={"type": "page_id", "page_id": directory_name},
            title=[{"type": "text", "text": {"content": "New Directory"}}],
            properties={}
        )
        print(f"Directory created: {response}")

    def set_ready(self):
        print("NotionStorageService is ready")

    def teardown(self):
        print("NotionStorageService is being torn down")


class NotionStorageServiceFactory(ServiceFactory):
    def __init__(self, api_token: str, database_id: str):
        self.api_token = api_token
        self.database_id = database_id

    def create(self) -> NotionStorageService:
        return NotionStorageService(self.api_token, self.database_id)