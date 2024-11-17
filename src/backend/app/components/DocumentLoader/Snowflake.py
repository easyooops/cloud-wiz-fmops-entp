from app.components.DocumentLoader.Base import BaseDocumentLoader
from langchain_community.document_loaders import SnowflakeLoader

class SnowflakeDocumentLoader(BaseDocumentLoader):
    def __init__(self, config: dict, metadata_columns: list = None):
        super().__init__()
        self.metadata_columns = metadata_columns
        self.snowflake_loader = SnowflakeLoader(
            query=config['db_query'],
            user=config['db_user'],
            password=config['db_password'],
            account=config['db_account'],
            warehouse=config['db_warehouse'],
            role=config['db_role'],
            database=config['db_database'],
            schema=config['db_schema'],
            metadata_columns=self.metadata_columns,
        )

    def load(self):
        """Load documents from Snowflake."""
        self.documents = self.snowflake_loader.load()
        return self.documents

    def process_documents(self):
        """Process the documents if any additional processing is needed."""
        # Add any document processing steps here
        pass
