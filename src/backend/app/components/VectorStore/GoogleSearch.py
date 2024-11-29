import logging  
from app.components.VectorStore.Base import AbstractVectorStoreComponent
from google.cloud import aiplatform  
from google.cloud.aiplatform.matching_engine import MatchingEngineIndexEndpoint, MatchingEngineIndex  

class GoogleVertexAIVectorStoreComponent(AbstractVectorStoreComponent):  
    def __init__(self, project: str, location: str, index_id: str, endpoint_id: str):  
        super().__init__()  
        self.project = project  
        self.location = location  
        self.index_id = index_id  
        self.endpoint_id = endpoint_id  
        self.index = None  
        self.endpoint = None  
  
    def initialize(self):  
        aiplatform.init(project=self.project, location=self.location)  
        self.index = MatchingEngineIndex(self.index_id)  
        self.endpoint = MatchingEngineIndexEndpoint(self.endpoint_id)  
        logging.info(f"Initialized Google Vertex AI Vector Search with index {self.index_id} and endpoint {self.endpoint_id}")  
  
    def add_embeddings(self, embeddings: list):  
        try:  
            # Assuming embeddings is a list of dictionaries with 'id' and 'embedding' keys  
            for embedding in embeddings:  
                self.index.update(embedding['id'], embedding['embedding'])  
            logging.info(f"Added {len(embeddings)} embeddings to index {self.index_id}")  
        except Exception as e:  
            logging.error(f"Failed to add embeddings: {e}")  
  
    def query(self, query_vector: list[float], top_k: int):  
        try:  
            response = self.endpoint.match(query_vector, top_k=top_k)  
            return response.matches  
        except Exception as e:  
            logging.error(f"Query failed: {e}")  
            return []  
  
    def save_index(self, file_path, storage_location):  
        logging.info("Google Vertex AI manages index persistence automatically.")  
  
    def load_index(self, persist_directory):  
        logging.info("Google Vertex AI manages index loading automatically.")  
  
    def delete_index(self):  
        try:  
            self.index.delete()  
            logging.info(f"Index {self.index_id} deleted successfully.")  
        except Exception as e:  
            logging.error(f"Failed to delete index: {e}")  
  
    def clear_index(self):  
        self.delete_index()  
        self.initialize()  