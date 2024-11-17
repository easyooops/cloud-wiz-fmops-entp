import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_openai import OpenAIEmbeddings
from app.components.Embedding.Base import AbstractEmbeddingComponent

class OpenAIEmbeddingComponent(AbstractEmbeddingComponent):
    def __init__(self, openai_api_key: str):
        """
        Initialize the OpenAIEmbeddingComponent with an OpenAI API key.
        
        Args:
            openai_api_key (str): The OpenAI API key to use for authentication.
        """
        super().__init__()
        self.openai_api_key = openai_api_key
        self.model_instance = None
        self.executor = ThreadPoolExecutor()

    def build(self, model_id: str = "text-embedding-3-small", dimension: int = None):
        """
        Build and configure the model instance.
        
        Args:
            model_id (str): The model identifier to use. Defaults to "text-embedding-3-small".
        """
        self.model_instance = OpenAIEmbeddings(
            openai_api_key=self.openai_api_key,
            dimensions=dimension,
            model=model_id
        )

    async def run_embed_query(self, input_text: str) -> list[float]:
        """
        Embed a single query text into a vector of floats.
        
        Args:
            input_text (str): The text to embed.
        
        Returns:
            list[float]: The resulting embedding vector.
        
        Raises:
            ValueError: If the model instance is not initialized or the result is unexpected.
        """
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the build method first.")
        
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(self.executor, self.model_instance.embed_query, input_text)
            if isinstance(result, list) and all(isinstance(i, float) for i in result):
                return result
            else:
                raise ValueError("Unexpected return type from embed_query")
        except Exception as e:
            raise RuntimeError(f"An error occurred while embedding the query: {e}")

    async def run_embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Embed multiple documents into vectors of floats.
        
        Args:
            documents (list[str]): The documents to embed.
        
        Returns:
            list[list[float]]: The resulting list of embedding vectors.
        
        Raises:
            ValueError: If the model instance is not initialized.
        """
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the build method first.")
        
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(self.executor, self.model_instance.embed_documents, documents)
        except Exception as e:
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")

    async def embed_documents(self, documents: list[str]) -> list[list[float]]:
        """
        Embed multiple documents into vectors of floats.
        
        Args:
            documents (list[str]): The documents to embed.
        
        Returns:
            list[list[float]]: The resulting list of embedding vectors.
        
        Raises:
            ValueError: If the model instance is not initialized.
        """
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the build method first.")
        
        loop = asyncio.get_event_loop()
        try:
            return await loop.run_in_executor(self.executor, self.model_instance.embed_documents, documents)
        except Exception as e:
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")
        
    def __del__(self):
        """
        Destructor to clean up resources.
        """
        self.executor.shutdown()
