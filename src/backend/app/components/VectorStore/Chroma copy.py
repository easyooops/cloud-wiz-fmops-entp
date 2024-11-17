import asyncio
import os
import logging
from app.components.VectorStore.Base import AbstractVectorStoreComponent
from langchain_chroma import Chroma
from langchain.docstore.document import Document
from langchain_community.vectorstores.utils import filter_complex_metadata

class ChromaVectorStoreComponent(AbstractVectorStoreComponent):
    def __init__(self, storage_service=None):
        super().__init__()
        self.embedding_function = None
        self.db = None
        self.persist_directory = None
        self.docs = None
        self.index_name = None
        self.storage_service = storage_service
        self.embed_component = None

    async def initialize(self, docs, embed_component, persist_directory=None, index_name=None):
        """
        Initialize the vector store with documents, embedding component, directory, and index name.
        
        Args:
            docs: Documents to initialize the vector store with.
            embed_component: The embedding component to use (OpenAIEmbeddingComponent or BedrockEmbeddingComponent).
            persist_directory: Directory to persist the index.
            index_name: Name of the index.
        """
        self.embed_component = embed_component
        self.persist_directory = persist_directory
        self.docs = docs
        self.index_name = index_name

        # embeddings = await embed_component.run_embed_documents([doc.page_content for doc in docs])
        # docs_with_embeddings = [
        #     Document(page_content=doc.page_content, metadata={"embedding": embedding})
        #     for doc, embedding in zip(docs, embeddings)
        # ]

        # simple_docs = filter_complex_metadata(docs_with_embeddings)
        
        if persist_directory:
            self.db = Chroma.from_documents(docs, embed_component, persist_directory, index_name)
        else:
            self.db = Chroma.from_documents(docs, embed_component, index_name)

    async def add_embeddings(self, docs):
        """
        Add embeddings for additional documents.
        
        Args:
            docs: Documents to add embeddings for.
        
        Raises:
            ValueError: If the database is not initialized.
        """
        if self.db:
            embeddings = await self.embed_component.run_embed_documents([doc.page_content for doc in docs])
            docs_with_embeddings = [
                Document(page_content=doc.page_content, metadata={"embedding": embedding})
                for doc, embedding in zip(docs, embeddings)
            ]
            simple_docs = filter_complex_metadata(docs_with_embeddings)            
            self.db.add(simple_docs)
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def query(self, query, top_k: int):
        """
        Query the vector store for similar documents.
        
        Args:
            query: The query text.
            top_k: Number of top results to return.
        
        Returns:
            List of similar documents.
        
        Raises:
            ValueError: If the database is not initialized.
        """
        if self.db:
            results = self.db.similarity_search(query, top_k=top_k)
            return results
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def save_index(self, storage_location):
        """
        Save the index to a storage location.
        
        Args:
            storage_location: Location to save the index to.
        
        Raises:
            ValueError: If the persist directory is not set or the database is not initialized.
        """
        if self.db:
            logging.info(f"Saving index to {storage_location}")
            if not self.persist_directory:
                raise ValueError("Persist directory is not set.")
            
            if self.storage_service:
                for file_name in os.listdir(self.persist_directory):
                    file_path = os.path.join(self.persist_directory, file_name)
                    if os.path.isfile(file_path):
                        storage_file_path = os.path.join(storage_location, file_name)
                        with open(file_path, 'rb') as file:
                            self.storage_service.upload_file(file, storage_file_path)
        else:
            raise ValueError("Database is not initialized. Call the initialize method first.")

    def load_index(self, storage_location, persist_directory, embed_component):
        """
        Load an index from a storage location.
        
        Args:
            storage_location: Location to load the index from.
            persist_directory: Directory to persist the index.
        """
        if self.storage_service:
            os.makedirs(persist_directory, exist_ok=True)
            files = self.storage_service.list_files(storage_location)
            for file in files:
                file_name = os.path.basename(file['Key'])
                file_path = os.path.join(persist_directory, file_name)
                self.storage_service.download_file(file['Key'], file_path)
                
            return Chroma(persist_directory, embed_component.embed_documents)
