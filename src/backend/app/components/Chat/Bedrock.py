import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from app.components.Chat.Base import AbstractLLMComponent

class ChatBedrockComponent(AbstractLLMComponent):
    def __init__(self, aws_access_key, aws_secret_access_key, aws_region):
        super().__init__()
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

        self.boto3_session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )

    def build(self, model_id: str, temperature: float, top_p: float = None, max_tokens: int = None):
        
        if not model_id:
            model_id = "amazon.titan-text-express-v1"

        model_kwargs = {"temperature": temperature, "top_p": top_p, "max_tokens":max_tokens}

        if "amazon" in model_id:
            del model_kwargs["top_p"]
            del model_kwargs["max_tokens"]

        if "meta" in model_id:
            del model_kwargs["max_tokens"]

        self.model_instance = ChatBedrock(
            client=self.boto3_session.client('bedrock-runtime'),
            model_id=model_id,
            model_kwargs=model_kwargs
        )

    def run(self, prompt):
        if self.model_instance is None:
            raise ValueError("Model instance is not initialized. Call the configure method first.")
        human_message = HumanMessage(content=prompt)
        response = self.model_instance.invoke([human_message])
        return response.content
