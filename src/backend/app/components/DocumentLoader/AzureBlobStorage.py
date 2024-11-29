from langchain_community.document_loaders import AzureBlobStorageContainerLoader  
from app.components.DocumentLoader.Base import BaseDocumentLoader  
  
class AzureBlobStorageLoader(BaseDocumentLoader):  
    def __init__(self, account_name, account_key, container_name, directory_path=None):  
        super().__init__()  
        self.account_name = account_name  
        self.account_key = account_key  
        self.container_name = container_name  
        self.prefix = directory_path  
  
    def load(self):  
        conn_str = (  
            f"DefaultEndpointsProtocol=https;"  
            f"AccountName={self.account_name};"  
            f"AccountKey={self.account_key};"  
            f"EndpointSuffix=core.windows.net"  
        )  
        self.loader = AzureBlobStorageContainerLoader(  
            conn_str=conn_str,  
            container=self.container_name,  
            prefix=self.prefix  
        )  
        self.documents = self.loader.load()  
  
    def process_documents(self):  
        if not self.documents:  
            raise ValueError("Documents are not loaded yet. Call the load method first.")  
          
        processed_documents = []  
        for doc in self.documents:  
            processed_documents.append(doc.page_content)  
        self.documents = processed_documents  
  
    def get_documents(self):  
        return super().get_documents()  