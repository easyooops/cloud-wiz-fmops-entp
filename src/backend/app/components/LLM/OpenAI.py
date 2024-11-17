from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from app.components.LLM.Base import BaseLLMComponent

class OpenAILLMComponent(BaseLLMComponent):
    def __init__(self, openai_api_key):
        super().__init__()
        self.openai_api_key = openai_api_key

    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):

        if not model_id:
            model_id="gpt-3.5-turbo-instruct"

        self.model_instance = OpenAI(
            openai_api_key=self.openai_api_key, 
            model=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            streaming=True
        )

    def run(self, prompt):
        if self.model_instance is None:
            raise ValueError("LLM is not initialized. Call the build method first.")
        return self.model_instance.invoke(prompt)   