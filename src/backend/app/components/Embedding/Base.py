from langchain_openai import OpenAIEmbeddings


class AbstractEmbeddingComponent:
    def __init__(self):
        self.model_instance = None

    def build(self, **kwargs):
        raise NotImplementedError("The configure method needs to be implemented")

    def run(self, input_text):
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the configure method first.")
        return self.model_instance(input_text)

    def run_embed_query(self, input_text):
        raise NotImplementedError("The run_embed_query method needs to be implemented")

    async def run_embed_documents(self, documents: list):
        raise NotImplementedError("The run_embed_documents method needs to be implemented")

    async def embed_documents(self, documents: list):
        raise NotImplementedError("The run_embed_documents method needs to be implemented")