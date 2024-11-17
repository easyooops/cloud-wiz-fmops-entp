from langchain_google_genai import GoogleGenerativeAI
from app.components.LLM.Base import BaseLLMComponent

class GoogleAILLMComponent(BaseLLMComponent):
    def __init__(self, google_api_key):
        super().__init__()
        self.google_api_key = google_api_key

    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):

        if not model_id:
            model_id="gemini-pro"

        self.model_instance = GoogleGenerativeAI(
            google_api_key=self.google_api_key,
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