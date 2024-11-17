from app.components.DocumentLoader.Base import BaseDocumentLoader
from langchain_community.document_loaders import NotionDBLoader

class NotionDocumentLoader(BaseDocumentLoader):
    def __init__(self, config: dict):
        super().__init__()
        self.notion_loader = NotionDBLoader(
            integration_token=config['api_token'],
            database_id=config['db_database'],
            request_timeout_sec=30
        )

    def load(self):
        """Load documents from Notion."""
        self.documents = self.notion_loader.load()
        return self.documents

    def process_documents(self):
        """Process the documents if any additional processing is needed."""
        # Add any document processing steps here
        pass
