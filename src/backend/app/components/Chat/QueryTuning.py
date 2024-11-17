from app.components.Chat.Base import AbstractLLMComponent
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

class QueryTuningComponent(AbstractLLMComponent):
    def __init__(self, openai_api_key):
        super().__init__()
        self.openai_api_key = openai_api_key

    def build(self, temperature=0.7):
        template = """Identify the query type and refine it if necessary. Query: {query}"""
        self.prompt = PromptTemplate.from_template(template)
        self.llm = OpenAI(openai_api_key=self.openai_api_key, temperature=temperature)

    def run(self, prompt):
        if self.llm is None:
            raise ValueError("LLM is not initialized. Call the configure method first.")
        refined_query = self.prompt | self.llm
        response = refined_query.invoke(prompt)
        return response['content'] if 'content' in response else response