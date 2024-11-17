from pydantic import BaseModel
from typing import List

class EmbeddingResponse(BaseModel):
    embedding: List[float]

class EmbeddingMultipleResponse(BaseModel):
    embeddings: List[List[float]]
