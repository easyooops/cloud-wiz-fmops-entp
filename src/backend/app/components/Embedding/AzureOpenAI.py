from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings  
from app.components.Embedding.Base import AbstractEmbeddingComponent  
  
class AzureOpenAIEmbeddingComponent(AbstractEmbeddingComponent):  
    def __init__(self, openai_api_version, azure_endpoint, api_key):  
        super().__init__()
        self.openai_api_version = openai_api_version  
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
  
    def build(self):
        self.model_instance = AzureOpenAIEmbeddings(
            azure_endpoint=self.azure_endpoint,  
            api_key=self.api_key,            
            openai_api_version=self.openai_api_version
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