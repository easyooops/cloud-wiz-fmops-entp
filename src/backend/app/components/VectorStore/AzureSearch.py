import logging  
from langchain.vectorstores import AzureSearch  
from langchain.schema import Document  
  
class AzureSearchVectorStoreComponent:  
    def __init__(self, endpoint: str, api_key: str, index_name: str, embeddings):  
        self.endpoint = endpoint  
        self.api_key = api_key  
        self.index_name = index_name  
        self.embeddings = embeddings
        self.vector_store = None
  
    def initialize(self):  
        try:  
            self.vector_store = AzureSearch(  
                        azure_search_endpoint=self.endpoint,  
                        azure_search_key=self.api_key,  
                        index_name=self.index_name,  
                        embedding_function=self.embeddings.run_embed_query  
                    )  
            logging.info(f"Index {self.index_name} initialized successfully.")  
        except Exception as e:  
            logging.error(f"Failed to initialize index: {e}")  
  
    def add_embeddings(self, documents):  
        try: 
            self.vector_store.add_documents(documents=documents)  
            logging.info(f"Added {len(documents)} embeddings to index {self.index_name}")  
        except Exception as e:  
            logging.error(f"Failed to add embeddings: {e}")  
  
    def query(self, query: str, top_k: int):  
        try:  
            results = self.vector_store.similarity_search(query=query, k=top_k)  
            return [result for result in results]  
        except Exception as e:  
            logging.error(f"Query failed: {e}")  
            return []  
  
    def delete_index(self):  
        try:  
            self.vector_store.delete_index()  
            logging.info(f"Index {self.index_name} deleted successfully.")  
        except Exception as e:  
            logging.error(f"Failed to delete index: {e}")  
  
    def clear_index(self):  
        self.delete_index()  
        self.initialize()  