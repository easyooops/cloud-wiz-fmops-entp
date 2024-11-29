from google.auth import load_credentials_from_file  
from langchain_google_vertexai.embeddings import VertexAIEmbeddings  
from app.components.Embedding.Base import AbstractEmbeddingComponent  
  
class GoogleVertexAIEmbeddingComponent(AbstractEmbeddingComponent):  
    def __init__(self, project_id, location, credentials_path=None):  
        super().__init__()  
        self.project_id = project_id  
        self.location = location  
        self.credentials_path = credentials_path  
  
        if self.credentials_path:  
            self.credentials, self.project = load_credentials_from_file(self.credentials_path)  
        else:  
            self.credentials = None  
  
    def build(self, model_id: str = "textembedding-gecko-001"):  
        self.model_instance = VertexAIEmbeddings(  
            model=model_id,  
            project=self.project_id,  
            location=self.location,  
            credentials=self.credentials  
        )  
  
    def run_embed_query(self, input_text: str) -> list[float]:  
        if self.model_instance is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
          
        try:  
            result = self.model_instance.embed_query(input_text)  
            if isinstance(result, list) and all(isinstance(i, float) for i in result):  
                return result  
            else:  
                raise ValueError("Unexpected return type from embed_query")  
        except Exception as e:  
            raise RuntimeError(f"An error occurred while embedding the query: {e}")  
  
    async def run_embed_documents(self, documents: list[str]) -> list[list[float]]:  
        if self.model_instance is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
          
        try:  
            return await self.model_instance.aembed_documents(documents)  
        except Exception as e:  
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")  
  
    async def embed_documents(self, documents: list[str]) -> list[list[float]]:  
        if self.model_instance is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
          
        try:  
            return await self.model_instance.aembed_documents(documents)  
        except Exception as e:  
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")  