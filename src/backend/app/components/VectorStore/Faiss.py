import json
import logging
import os
from langchain_community.vectorstores import FAISS
import faiss
import numpy as np
from app.components.VectorStore.Base import AbstractVectorStoreComponent

class FaissVectorStoreComponent(AbstractVectorStoreComponent):
    def __init__(self, storage_service=None, embedding_function=None):
        super().__init__()
        self.dimension = None
        self.storage_service = storage_service
        self.embedding_function = embedding_function  # embedding_function 추가
        self.index = None
        self.document_texts = []

    def initialize(self, dimension):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)

    def add_embeddings(self, embeddings: list, docs: list):
        vectors = np.array(embeddings).astype('float32')
        if vectors.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimensions do not match. Expected {self.dimension}, got {vectors.shape[1]}")
        self.index.add(vectors)
        self.document_texts = [doc.page_content for doc in docs]
        logging.info(f"Added {len(docs)} documents to the FAISS index.")

    def query(self, query_vector: list[float], top_k: int):
        query_vector_np = np.array([query_vector]).astype('float32')
        distances, indices = self.index.search(query_vector_np, top_k)
        return indices[0], distances[0]

    def save_index(self, file_path, storage_location):
        if self.index:
            # Save FAISS index to local file
            faiss.write_index(self.index, file_path)
            # Upload to storage service
            if self.storage_service:
                with open(file_path, 'rb') as f:
                    self.storage_service.upload_file(f, storage_location)
            os.remove(file_path)
        else:
            raise ValueError("Index is not initialized.")

    def load_index(self, storage_location, file_path):
        # Download FAISS index from storage service to local file
        self.storage_service.download_file(storage_location, file_path)
        # Load FAISS index from local file
        self.index = faiss.read_index(file_path)
        os.remove(file_path)