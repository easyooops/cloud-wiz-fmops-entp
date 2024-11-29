import logging

import os
from uuid import UUID
from fastapi import HTTPException
from langchain_text_splitters import CharacterTextSplitter
from sqlmodel import Session

from app.components.VectorStore.Chroma import ChromaVectorStoreComponent
from app.components.Embedding.Bedrock import BedrockEmbeddingComponent  
from app.components.Embedding.AzureOpenAI import AzureOpenAIEmbeddingComponent
from app.components.Embedding.GoogleVertexAI import GoogleVertexAIEmbeddingComponent
from app.components.VectorStore.AWSOpenSearch import OpenSearchVectorStoreComponent
from app.components.VectorStore.AzureSearch import AzureSearchVectorStoreComponent
from app.components.VectorStore.GoogleSearch import GoogleVertexAIVectorStoreComponent
from app.service.store.service import StoreService
from app.components.DocumentLoader.AzureBlobStorage import AzureBlobStorageLoader
from app.components.DocumentLoader.GCS import GCSDocumentLoader
from app.components.DocumentLoader.S3 import S3DocumentLoader
from app.service.store.model import Store

class EmbeddingService():
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def load_documents(self, full_directory_name: str = ''):  
        documents = []  
        csp_provider = os.getenv("CSP_PROVIDER")
        
        if csp_provider == "azure":  
            loader = AzureBlobStorageLoader(  
                account_name=os.getenv("AZURE_STORAGE_ACCOUNT_NAME"), 
                account_key=os.getenv("AZURE_STORAGE_ACCOUNT_KEY") , 
                container_name=os.getenv("AZURE_STORAGE_CONTAINER_NAME"),
                directory_path=full_directory_name
            )  
        elif csp_provider == "aws":  
            loader = S3DocumentLoader(  
                bucket_name=os.getenv("STORE_NAME"),  
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),  
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),  
                region_name=os.getenv("AWS_REGION"),
                directory_path=full_directory_name 
            )  
        elif csp_provider == "gcp":  
            loader = GCSDocumentLoader(  
                bucket_name=os.getenv("STORE_NAME"), 
                project_id=os.getenv("GCP_PROJECT_ID"),  
                credentials=None,
                directory_path=full_directory_name
            )  
        else:  
            raise ValueError("Unsupported CSP provider")  
    
        loader.load() 
        documents = loader.get_documents()  
        return documents  
        
    def create_indexing(self, user_id: UUID, store_id: UUID):  
        try:
            # 스토리지 경로 정보 로드
            store = self.session.get(Store, store_id)  
            if not store:  
                raise HTTPException(status_code=404, detail="Store not found")  
            full_directory_name = f"{user_id}/{store.store_name}" 
                        
            # 문서 로드  
            csp_provider = os.getenv("CSP_PROVIDER")  
            documents = self.load_documents(full_directory_name) 
                
            # 문서를 1000 단위로 청킹  
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)  
            # chunked_docs = [chunk for chunk in text_splitter.split_documents(documents) if chunk.page_content]  
            chunked_docs = text_splitter.split_documents(documents)
                    
            embed_component = self._initialize_embedding_component(csp_provider)
            embed_component.build()  
                            
            # Azure AI Search
            if csp_provider == "azure":  
                # 임베딩
                azure_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")  
                azure_api_key = os.getenv("AZURE_SEARCH_API_KEY")              
                
                # 벡터 스토어
                index_name = f"{store_id}_index"
                vector_store = AzureSearchVectorStoreComponent(azure_endpoint, azure_api_key, index_name, embed_component)  
                vector_store.initialize()  
                vector_store.add_embeddings(chunked_docs)
            
            # AWS OpenSearch
            elif csp_provider == "aws":  
                host = os.getenv("AWS_OPENSEARCH_HOST")  
                port = 9200  
                username = os.getenv("AWS_OPENSEARCH_USERNAME")  
                password = os.getenv("AWS_OPENSEARCH_PASSWORD")  
                index_name = f"{store_id}_index"  
                index_config = {  
                    "settings": {  
                        "number_of_shards": 1,  
                        "number_of_replicas": 0  
                    },  
                    "mappings": {  
                        "properties": {  
                            "id": {"type": "keyword"},  
                            "embedding": {"type": "knn_vector", "dimension": 128}  # Adjust dimension as needed  
                        }  
                    }  
                }  
                vector_store = OpenSearchVectorStoreComponent(host, port, username, password, index_name)  
                vector_store.initialize(index_config=index_config)  
                vector_store.add_embeddings(chunked_docs) 
            
            # GCP Vector Search
            elif csp_provider == "gcp":  
                project = os.getenv("GCP_PROJECT")  
                location = os.getenv("GCP_LOCATION")  
                index_id = f"{store_id}_index"  
                endpoint_id = os.getenv("GCP_ENDPOINT_ID")  
                vector_store = GoogleVertexAIVectorStoreComponent(project, location, index_id, endpoint_id)  
                vector_store.initialize()  
                vector_store.add_embeddings(chunked_docs)  
            
            # Default to Chroma 
            else: 
                persist_directory = f"./chroma_db/{store_id}"  
                vector_store = ChromaVectorStoreComponent()  
                vector_store.initialize(docs=chunked_docs, embedding_function=embed_component.model_instance, persist_directory=persist_directory, index_name=str(agent_data.storage_provider_id))  
                
            return {"status": "success", "message": "Indexing completed successfully."}
        
        except Exception as e:  
            logging.error(f"Error creating indexing: {str(e)}")  
            raise HTTPException(status_code=500, detail=f"Error creating indexing: {str(e)}")  

    def _initialize_embedding_component(self, csp_provider: str):  
        """Initialize the embedding component based on the embedding type.  
        Args:  
            csp_provider (str): Type of embedding provider (e.g., "azure" for OpenAI, "aws" for Bedrock, "gcp" for Google VertexAI).  
        Returns:  
            Any: The initialized embedding component.  
        Raises:  
            ValueError: If required credentials are missing.  
        """  
        # Azure OpenAI Embedding
        if csp_provider == "azure":  
            azure_endpoint = os.getenv("AZURE_OPENAI_API_ENDPOINT")  
            openai_api_version = os.getenv("AZURE_OPENAI_API_EMBED_VERSION")  
            api_key = os.getenv("AZURE_OPENAI_API_KEY")  
            if not all([openai_api_version, azure_endpoint, api_key]):  
                raise ValueError("Azure OpenAI credentials are not set in the environment variables.")  
            return AzureOpenAIEmbeddingComponent(openai_api_version, azure_endpoint, api_key)  
  
        # AWS Bedrock Embedding
        elif csp_provider == "aws":  
            aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")  
            aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")  
            aws_region = os.getenv("AWS_REGION")  
            if not all([aws_access_key, aws_secret_access_key, aws_region]):  
                raise ValueError("AWS credentials or region are not set in the environment variables.")  
            return BedrockEmbeddingComponent(aws_access_key, aws_secret_access_key, aws_region)  
  
        # Google VertexAI Embedding
        elif csp_provider == "gcp":  
            project_id = os.getenv("GCP_PROJECT_ID")  
            location = os.getenv("GCP_LOCATION")  
            credentials_path = os.getenv("GCP_CREDENTIALS_PATH")  
            if not all([project_id, location, credentials_path]):  
                raise ValueError("Google VertexAI credentials are not set in the environment variables.")  
            return GoogleVertexAIEmbeddingComponent(project_id, location, credentials_path)  
  
        else:  
            raise ValueError(f"Unsupported embedding type: {csp_provider}")
        
    async def _run_embedding_main(self, agent_data):  
        csp_provider = os.getenv("CSP_PROVIDER")  
          
        if csp_provider == "azure":  
            return await self._run_embedding_azure_search(agent_data)  
        elif csp_provider == "aws":  
            return await self._run_embedding_aws_opensearch(agent_data)  
        elif csp_provider == "gcp":  
            return await self._run_embedding_google_vertexai(agent_data)  
        else:  
            return await self._run_embedding_chroma(agent_data)  
  
    async def _run_embedding_chroma(self, agent_data):  
        """Load the Chroma engine for querying.  
        Args:  
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.  
        Returns:  
            Any: The Chroma engine or an error message.  
        """  
        agents_store = agent_data['Agent']        
        try:  
            csp_provider = os.getenv("CSP_PROVIDER")  
            embed_component = self._initialize_embedding_component(csp_provider)
            embed_component.build()  
            persist_directory = f"./chroma_db/{agents_store.storage_provider_id}"  
            chroma_component = ChromaVectorStoreComponent()  
            chroma_component.embedding_function = embed_component.model_instance  
            chroma_component.load_index(persist_directory)  
            if chroma_component.db:  
                logging.warning("Database initialized successfully.")  
            else:  
                logging.warning("Database initialization failed.")  
            return chroma_component.db  
        except Exception as e:  
            logging.error(f"An error occurred while loading the Chroma engine: {e}")  
            return f"An error occurred: {e}"  
  
    async def _run_embedding_aws_opensearch(self, agent_data):  
        """Load the AWS OpenSearch engine for querying.  
        Args:  
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.  
        Returns:  
            Any: The AWS OpenSearch engine or an error message.  
        """  
        agents_store = agent_data['Agent'] 
        try:  
            csp_provider = os.getenv("CSP_PROVIDER")  
            embed_component = self._initialize_embedding_component(csp_provider)
            embed_component.build()  
              
            # AWS OpenSearch initialization  
            host = os.getenv("AWS_OPENSEARCH_HOST")  
            port = 9200  
            username = os.getenv("AWS_OPENSEARCH_USERNAME")  
            password = os.getenv("AWS_OPENSEARCH_PASSWORD")  
            index_name = f"{agents_store.storage_object_id}_index"  
            vector_store = OpenSearchVectorStoreComponent(host, port, username, password, index_name, embed_component)  
            vector_store.load_index()  
              
            if vector_store.db:  
                logging.warning("Database initialized successfully.")  
            else:  
                logging.warning("Database initialization failed.")  
            return vector_store.db  
        except Exception as e:  
            logging.error(f"An error occurred while loading the AWS OpenSearch engine: {e}")  
            return f"An error occurred: {e}"  
  
    async def _run_embedding_azure_search(self, agent_data):  
        """Load the Azure Search engine for querying.  
        Args:  
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.  
        Returns:  
            Any: The Azure Search engine or an error message.  
        """  
        agents_store = agent_data['Agent']
        try:  
            csp_provider = os.getenv("CSP_PROVIDER")  
            embed_component = self._initialize_embedding_component(csp_provider)
            embed_component.build()    
              
            # Azure Search initialization  
            azure_endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")  
            azure_api_key = os.getenv("AZURE_SEARCH_API_KEY")  
            index_name = f"{agents_store.storage_object_id}_index"  
            vector_store = AzureSearchVectorStoreComponent(azure_endpoint, azure_api_key, index_name, embed_component)  
            vector_store.initialize()
              
            if vector_store.vector_store:  
                logging.warning("Database initialized successfully.")  
            else:  
                logging.warning("Database initialization failed.")  
            return vector_store.vector_store 
        except Exception as e:  
            logging.error(f"An error occurred while loading the Azure Search engine: {e}")  
            return f"An error occurred: {e}"  
  
    async def _run_embedding_google_vertexai(self, agent_data):  
        """Load the Google Vertex AI engine for querying.  
        Args:  
            agent_data (Dict[str, Any]): Dictionary containing agent-related data.  
        Returns:  
            Any: The Google Vertex AI engine or an error message.  
        """  
        agents_store = agent_data['Agent']  
        try: 
            csp_provider = os.getenv("CSP_PROVIDER")  
            embed_component = self._initialize_embedding_component(csp_provider) 
            embed_component.build()
              
            # Google Vertex AI initialization  
            project = os.getenv("GCP_PROJECT")  
            location = os.getenv("GCP_LOCATION")  
            index_id = f"{agents_store.storage_object_id}_index"  
            endpoint_id = os.getenv("GCP_ENDPOINT_ID")  
            vector_store = GoogleVertexAIVectorStoreComponent(project, location, index_id, endpoint_id, embed_component)  
            vector_store.load_index()  
              
            if vector_store.db:  
                logging.warning("Database initialized successfully.")  
            else:  
                logging.warning("Database initialization failed.")  
            return vector_store.db  
        except Exception as e:  
            logging.error(f"An error occurred while loading the Google Vertex AI engine: {e}")  
            return f"An error occurred: {e}"  