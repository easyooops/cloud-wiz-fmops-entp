from langchain_openai import AzureChatOpenAI  
from app.components.Chat.Base import AbstractLLMComponent  
  
class ChatOpenAIComponent(AbstractLLMComponent):  
    def __init__(self, openai_api_version, azure_endpoint, api_key, model_id):  
        super().__init__()  
        self.openai_api_version = openai_api_version  
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.model_id = model_id
        self.model_instance = None  
  
    def build(self, temperature: float = None, top_p: float = None):  

        model_kwargs = {  
            "azure_deployment": self.model_id,  
            "azure_endpoint": self.azure_endpoint,  
            "api_version": self.openai_api_version,  
            "api_key": self.api_key,
            "temperature": temperature,  
            "top_p": top_p
        }  
          
        self.model_instance = AzureChatOpenAI(**model_kwargs)  
  
    def run(self, prompt):  
        if self.model_instance is None:  
            raise ValueError("Model instance is not initialized. Call the build method first.")  
        
        response = self.model_instance.invoke(prompt)  
        return response.content