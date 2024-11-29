from google.cloud import storage  
from google.auth.exceptions import DefaultCredentialsError  
from app.components.DocumentLoader.Base import BaseDocumentLoader
  
class GCSDocumentLoader(BaseDocumentLoader):  
    def __init__(self, bucket_name, prefix=None, project_id=None, credentials=None):  
        super().__init__()  
        self.bucket_name = bucket_name  
        self.prefix = prefix  
        self.client = storage.Client(project=project_id, credentials=credentials)  
        self.bucket = self.client.bucket(bucket_name)  
  
    def load(self):  
        try:  
            if self.prefix:  
                blobs = self.bucket.list_blobs(prefix=self.prefix)  
            else:  
                blobs = self.bucket.list_blobs()  
  
            self.documents = []  
  
            for blob in blobs:  
                content = blob.download_as_bytes()  
                self.documents.append(content)  
  
        except DefaultCredentialsError:  
            raise ValueError("GCP credentials not provided or not configured correctly.")  
        except Exception as e:  
            raise ValueError(f"An error occurred: {str(e)}")  
  
    def process_documents(self):  
        if self.documents is None:  
            raise ValueError("Documents are not loaded yet. Call the load method first.")  
        # 예시로, 문서의 내용을 텍스트로 변환하여 저장하는 과정  
        processed_documents = []  
        for doc in self.documents:  
            processed_documents.append(doc.decode("utf-8"))  
        self.documents = processed_documents