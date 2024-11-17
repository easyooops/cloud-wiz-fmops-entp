import asyncio

from langchain_google_genai import ChatGoogleGenerativeAI
from app.components.Chat.Base import AbstractLLMComponent

class ChatGoogleAIComponent(AbstractLLMComponent):
    def __init__(self, google_api_key):
        super().__init__()
        self.google_api_key = google_api_key

    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):
        if not model_id:
            model_id = "gemini-1.5-pro"

        self.model_instance = ChatGoogleGenerativeAI(
            api_key=self.google_api_key,
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
