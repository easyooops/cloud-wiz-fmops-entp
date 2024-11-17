import logging
import time
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from app.components.VectorStore.Base import AbstractVectorStoreComponent

class PineconeVectorStoreComponent(AbstractVectorStoreComponent):
    def __init__(self, api_key, environment, index_name):
        super().__init__()
        self.embedding_function = None
        self.index_name = index_name
        self.pinecone_client = Pinecone(api_key=api_key)
        self.environment = environment
        self.dimension = None
        self.db = None
        self.docs = None

    def initialize(self, docs, embedding_function):
        self.embedding_function = embedding_function
        self.docs = docs

        # Create or connect to the Pinecone index
        existing_indexes = [index_info["name"] for index_info in self.pinecone_client.list_indexes()]

        if self.index_name in existing_indexes:
            self.pinecone_client.delete_index(self.index_name)

        self.pinecone_client.create_index(
            name=self.index_name, 
            dimension=self.dimension,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region=self.environment)
        )
        while not self.pinecone_client.describe_index(self.index_name).status["ready"]:
            time.sleep(1)

        self.db = PineconeVectorStore.from_documents(
            documents=self.docs,
            embedding=self.embedding_function,
            index_name=self.index_name
        )
        

    def add_embeddings(self, docs):
        if self.db:
            self.db.add(docs)
        else:
            raise ValueError("Database is not initialized. Call the initialize or load_index method first.")

    def query(self, query, top_k: int):
        if self.db:
            results = self.db.similarity_search(query, top_k=top_k)
            return results
        else:
            raise ValueError("Database is not initialized. Call the initialize or load_index method first.")

    def save_index(self, storage_location):
        pass
    
    def reset_index(self):
        if self.index_name:
            self.pinecone_client.delete_index(self.index_name)
            self.pinecone_client.create_index(
                name=self.index_name, 
                dimension=self.dimension,
                metric="cosine"
            )

    def clear_index(self):
        if self.index_name:
            self.pinecone_client.delete_index(self.index_name)
        else:
            raise ValueError("Index name is not set.")

    def load_index(self, embedding_function):
        self.embedding_function = embedding_function

        # Connect to the existing Pinecone index
        existing_indexes = [index_info["name"] for index_info in self.pinecone_client.list_indexes()]

        if self.index_name in existing_indexes:
            self.db = PineconeVectorStore(
                index_name=self.index_name, 
                embedding=self.embedding_function
            )
            # self.db = PineconeVectorStore.from_documents(
            #     index_name=self.index_name, 
            #     embedding=self.embedding_function
            # )
        else:
            raise ValueError(f"Index {self.index_name} does not exist. Initialize the index first.")