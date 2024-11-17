from langchain_community.llms import Ollama
from app.components.LLM.Base import BaseLLMComponent

class OllamaLLMComponent(BaseLLMComponent):

    def __init__(self):
        super().__init__()

    def build(self):
        self.llm = Ollama(
            model="llama3"
        )

    def run(self, prompt):
        if self.llm is None:
            raise ValueError("LLM is not initialized. Call the build method first.")
        return self.llm.invoke(prompt)   