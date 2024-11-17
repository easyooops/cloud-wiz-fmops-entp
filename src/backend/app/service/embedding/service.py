import json
import os
from typing import List

import boto3
import faiss
import numpy as np
from sqlmodel import Session
from fastapi import HTTPException
from app.components.Embedding.Base import AbstractEmbeddingComponent
from app.components.Embedding.Bedrock import BedrockEmbeddingComponent
from app.components.Embedding.OpenAI import OpenAIEmbeddingComponent
from app.service.auth.service import AuthService
from app.components.VectorStore.Faiss import FaissVectorStoreComponent


class EmbeddingService:
    def __init__(self, session: Session):
        self.session = session
        self.faiss_store = None
        self.s3_client = boto3.client('s3')
        self.vector_store_bucket = os.getenv("AWS_S3_BUCKET_VECTOR_STORE_NAME")
        self.store_bucket = os.getenv("AWS_S3_BUCKET_STORE_NAME")

    def get_openai_embedding(self, text: str) -> List[float]:
        try:
            openai_api_key = AuthService.get_openai_key()
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the environment variables")

            embedding_component = OpenAIEmbeddingComponent(openai_api_key)
            embedding_component.build(model_id="text-embedding-ada-002")
            embedding = embedding_component.run_embed_query(text)
            return embedding
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_openai_embeddings(self, texts: list):
        try:
            openai_api_key = AuthService.get_openai_key()
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the environment variables")
            embedding_component = OpenAIEmbeddingComponent(openai_api_key)
            embedding_component.build(model_id="text-embedding-ada-002")
            embeddings = embedding_component.run_embed_documents(texts)
            return embeddings
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_bedrock_embedding(self, model_id: str, text: str):
        try:
            aws = AuthService.get_aws_key()
            aws_access_key = aws['aws_access_key']
            aws_secret_access_key = aws['aws_secret_access_key']
            aws_region = aws['aws_region']

            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the environment variables")

            embedding_component = BedrockEmbeddingComponent(
                aws_access_key=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_region=aws_region
            )
            embedding_component.build(model_id=model_id)
            embedding = embedding_component.run_embed_query(text)
            return embedding
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_bedrock_embeddings(self, model_id: str, texts: list):
        try:
            aws = AuthService.get_aws_key()
            aws_access_key = aws['aws_access_key']
            aws_secret_access_key = aws['aws_secret_access_key']
            aws_region = aws['aws_region']

            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the environment variables")

            embedding_component = BedrockEmbeddingComponent(
                aws_access_key=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_region=aws_region
            )
            embedding_component.build(model_id=model_id)
            embedding = embedding_component.run_embed_documents(texts)
            return embedding
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def initialize_faiss_store(self, embedding_component: AbstractEmbeddingComponent, dimension: int):
        self.faiss_store = FaissVectorStoreComponent()
        await self.faiss_store.initialize(dimension)

    async def add_to_faiss_store(self, texts: list):
        embeddings = self.get_openai_embeddings(texts)
        vectors = np.array(embeddings).astype('float32')
        return await self.faiss_store.add_embeddings(vectors)

    async def query_faiss_store(self, query_vector: list[float], top_k: int = 5):
        # print(f"Querying FAISS store with vector: {query_vector}")
        return await self.faiss_store.query(query_vector, top_k)

    def save_faiss_index_to_file(self, file_path: str):
        if self.faiss_store and self.faiss_store.index:
            faiss.write_index(self.faiss_store.index, file_path)
        else:
            raise ValueError("FAISS store is not initialized")

    def load_faiss_index_from_file(self, file_path: str):
        if not self.faiss_store:
            raise ValueError("FAISS store is not initialized")
        self.faiss_store.index = faiss.read_index(file_path)

    def save_faiss_index_to_s3(self, s3_file_path: str, local_file_path: str):
        self.save_faiss_index_to_file(local_file_path)
        self.s3_client.upload_file(local_file_path, self.vector_store_bucket, s3_file_path)

    def load_faiss_index_from_s3(self, s3_file_path: str, local_file_path: str):
        self.s3_client.download_file(self.vector_store_bucket, s3_file_path, local_file_path)
        self.load_faiss_index_from_file(local_file_path)
