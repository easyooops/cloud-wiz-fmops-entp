from abc import ABC, abstractmethod

class AbstractVectorStoreComponent(ABC):
    def __init__(self):
        self.index = None

    @abstractmethod
    def initialize(self, **kwargs):
        pass

    @abstractmethod
    def add_embeddings(self, embeddings: list):
        pass

    @abstractmethod
    def query(self, query_vector: list[float], top_k: int):
        pass

    @abstractmethod
    def save_index(self, file_path, storage_location):
        pass
