from google.auth import load_credentials_from_file  
from langchain_google_vertexai.chat_models import ChatVertexAI  
from langchain_core.messages import HumanMessage  
from app.components.Chat.Base import AbstractLLMComponent  
  
class ChatVertexAIComponent(AbstractLLMComponent):  
    def __init__(self, project_id, location, credentials_path=None):  
        super().__init__()  
        self.project_id = project_id  
        self.location = location  
        self.credentials_path = credentials_path  
  
        if self.credentials_path:  
            self.credentials, self.project = load_credentials_from_file(self.credentials_path)  
        else:  
            self.credentials = None  
  
    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):  
        if not model_id:  
            model_id = "text-bison-001"  
  
        model_kwargs = {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}  
  
        self.model_instance = ChatVertexAI(  
            model=model_id,  
            project=self.project_id,  
            location=self.location,  
            credentials=self.credentials,  
            **model_kwargs  
        )  
  
    def run(self, prompt):  
        if self.model_instance is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
          
        human_message = HumanMessage(content=prompt)  
        response = self.model_instance([human_message])  
        return response.content  
  