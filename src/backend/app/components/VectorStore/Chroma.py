import logging
import os
import shutil
import chromadb
from langchain_openai import OpenAIEmbeddings
from app.components.VectorStore.Base import AbstractVectorStoreComponent
from langchain_chroma import Chroma

class ChromaVectorStoreComponent(AbstractVectorStoreComponent):
    def __init__(self):
        super().__init__()
        self.embedding_function = None
        self.db = None
        self.persist_directory = None
        self.docs = None
        self.index_name = None

    def initialize(self, docs, embedding_function, persist_directory=None, index_name=None):
        self.embedding_function = embedding_function
        self.persist_directory = persist_directory
        self.docs = docs
        self.index_name = index_name

        self.db = Chroma.from_documents(
            documents=docs, 
            embedding=self.embedding_function,
            persist_directory=persist_directory
        )

    def add_embeddings(self, docs):
        if self.db:
            self.db.add(docs)
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def query(self, query, top_k: int):
        if self.db:
            results = self.db.similarity_search(query, top_k=top_k)
            return results
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def reset_index(self):
        if self.persist_directory and os.path.exists(self.persist_directory):
            # Remove existing index files
            for file in os.listdir(self.persist_directory):
                file_path = os.path.join(self.persist_directory, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        
        # Reinitialize the index with stored documents
        self.initialize(self.docs, self.embedding_function, persist_directory=self.persist_directory, index_name=self.index_name)

    def save_index(self):
        if self.db:
            if not self.persist_directory:
                raise ValueError("Persist directory is not set.")
            
            # 데이터베이스를 디스크에 저장
            self.db.save(persist_directory=self.persist_directory)

            logging.info(f"Index saved to {self.persist_directory}")
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def load_index(self, persist_directory):
        if not os.path.exists(persist_directory):
            raise ValueError(f"Persist directory {persist_directory} does not exist.")

        try:
            self.db = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embedding_function
            )
            logging.info(f"Index loaded from {persist_directory}")
        except Exception as e:
            logging.warning(f"Failed to load index from {persist_directory}: {e}")
            return None       

    def clear_persist_directory(self):
        """Helper function to clear the persist directory"""
        if self.persist_directory and os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
            os.makedirs(self.persist_directory)