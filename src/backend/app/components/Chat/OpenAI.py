import asyncio

from langchain_openai import ChatOpenAI
from app.components.Chat.Base import AbstractLLMComponent

class ChatOpenAIComponent(AbstractLLMComponent):
    def __init__(self, openai_api_key):
        super().__init__()
        self.openai_api_key = openai_api_key

    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):

        if not model_id:
            model_id="gpt-3.5-turbo"

        self.model_instance = ChatOpenAI(
            openai_api_key=self.openai_api_key, 
            model=model_id,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            streaming=True
        )

    def run(self, prompt):
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the configure method first.")
        response = self.model_instance.invoke(prompt)
        return response.content

    async def run_chat(self, prompt):
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the configure method first.")
        response = await asyncio.to_thread(self.model_instance.invoke, prompt)
        return response.content
