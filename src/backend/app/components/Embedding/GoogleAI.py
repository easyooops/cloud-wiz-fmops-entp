from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.components.Embedding.Base import AbstractEmbeddingComponent

class GoogleEmbeddingComponent(AbstractEmbeddingComponent):
    def __init__(self, google_api_key: str):
        """
        Initialize the GoogleEmbeddingComponent with a Google API key.
        
        Args:
            google_api_key (str): The Google API key to use for authentication.
        """
        super().__init__()
        self.google_api_key = google_api_key
        self.model_instance = None

    def build(self, model_id: str = "embedding-001", dimension: int = None):
        """
        Build and configure the model instance.
        
        Args:
            model_id (str): The model identifier to use. Defaults to "text-embedding-google-v1".
        """
        self.model_instance = GoogleGenerativeAIEmbeddings(
            google_api_key=self.google_api_key,
            dimensions=dimension,
            model="models/"+model_id
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
        
        try:
            result = self.model_instance.embed_query(input_text)
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
        
        try:
            return self.model_instance.embed_documents(documents)
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
        
        try:
            return self.model_instance.embed_documents(documents)
        except Exception as e:
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")
        
    def __del__(self):
        """
        Destructor to clean up resources.
        """
        # Add any necessary cleanup code here, if required
        pass
