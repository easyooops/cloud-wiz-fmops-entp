import logging  
from app.components.VectorStore.Base import AbstractVectorStoreComponent
from opensearchpy import OpenSearch, RequestsHttpConnection  
from requests.auth import HTTPBasicAuth  

class OpenSearchVectorStoreComponent(AbstractVectorStoreComponent):  
    def __init__(self, host: str, port: int, username: str, password: str, index_name: str):  
        super().__init__()  
        self.host = host  
        self.port = port  
        self.username = username  
        self.password = password  
        self.index_name = index_name  
        self.client = OpenSearch(  
            hosts=[{'host': self.host, 'port': self.port}],  
            http_auth=HTTPBasicAuth(self.username, self.password),  
            use_ssl=True,  
            verify_certs=True,  
            connection_class=RequestsHttpConnection  
        )  
  
    def initialize(self, index_config: dict):  
        self.index = self.index_name  
        if not self.client.indices.exists(index=self.index):  
            self.client.indices.create(index=self.index, body=index_config)  
            logging.info(f"Index {self.index} created with configuration: {index_config}")  
        else:  
            logging.info(f"Index {self.index} already exists.")  
  
    def add_embeddings(self, embeddings: list):  
        try:  
            actions = [  
                {"_op_type": "index", "_index": self.index, "_id": doc["id"], "_source": doc}  
                for doc in embeddings  
            ]  
            from opensearchpy.helpers import bulk  
            bulk(self.client, actions)  
            logging.info(f"Added {len(embeddings)} embeddings to index {self.index}")  
        except Exception as e:  
            logging.error(f"Failed to add embeddings: {e}")  
  
    def query(self, query_vector: list[float], top_k: int):  
        try:  
            body = {  
                "size": top_k,  
                "query": {  
                    "knn": {  
                        "field": "embedding",  
                        "query_vector": query_vector,  
                        "k": top_k  
                    }  
                }  
            }  
            response = self.client.search(index=self.index, body=body)  
            return response['hits']['hits']  
        except Exception as e:  
            logging.error(f"Query failed: {e}")  
            return []  
  
    def save_index(self, file_path, storage_location):  
        logging.info("OpenSearch manages index persistence automatically.")  
  
    def load_index(self, persist_directory):  
        logging.info("OpenSearch manages index loading automatically.")  
  
    def delete_index(self):  
        try:  
            self.client.indices.delete(index=self.index)  
            logging.info(f"Index {self.index} deleted successfully.")  
        except Exception as e:  
            logging.error(f"Failed to delete index: {e}")  
  
    def clear_index(self):  
        self.delete_index()  
        self.initialize({"settings": {"number_of_shards": 1, "number_of_replicas": 0}})  