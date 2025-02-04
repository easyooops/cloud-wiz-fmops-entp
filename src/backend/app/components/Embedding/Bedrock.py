import boto3
from app.components.Embedding.Base import AbstractEmbeddingComponent
from langchain_aws import BedrockEmbeddings

class BedrockEmbeddingComponent(AbstractEmbeddingComponent):
    def __init__(self, aws_access_key, aws_secret_access_key, aws_region, model_id, dimension):
        """
        Initialize the BedrockEmbeddingComponent with AWS credentials and region.
        
        Args:
            aws_access_key (str): AWS access key ID.
            aws_secret_access_key (str): AWS secret access key.
            aws_region (str): AWS region.
        """
        super().__init__()
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region
        self.model_id = model_id
        self.dimension = dimension

        self.boto3_session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )

        self.model_instance = None

    def build(self, model_id: str, dimension: int):
        """
        Build and configure the model instance.
        
        Args:
            model_id (str): The model identifier to use. Defaults to "amazon.titan-embed-text-v1".
        """
        if not model_id:
            raise ValueError("Model ID must be provided")
        if not dimension:
            raise ValueError("Dimension must be provided")

        self.model_instance = BedrockEmbeddings(
            model_id=self.model_id,
            dimension=self.dimension,
            client=self.boto3_session.client('bedrock-runtime')
        )

    def run_embed_query(self, input_text: str) -> list[float]:
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
            return await self.model_instance.aembed_documents(documents)
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
            return await self.model_instance.aembed_documents(documents)
        except Exception as e:
            raise RuntimeError(f"An error occurred while embedding the documents: {e}")
        
    def __del__(self):
        """
        Destructor to clean up resources.
        """
        # Add any necessary cleanup code here, if required
        pass
