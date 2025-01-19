import boto3
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage
from app.components.Chat.Base import AbstractLLMComponent

class ChatBedrockComponent(AbstractLLMComponent):
    def __init__(self, aws_access_key, aws_secret_access_key, aws_region, model_id):
        super().__init__()
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region
        self.model_id = model_id

        self.boto3_session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )

    def build(self, temperature: float, top_p: float = None, max_tokens: int = None):
        model_kwargs = {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}

        if "amazon" in self.model_id:
            model_kwargs.pop("top_p", None)
            model_kwargs.pop("max_tokens", None)

        if "meta" in self.model_id:
            model_kwargs.pop("max_tokens", None)

        self.model_instance = ChatBedrock(
            client=self.boto3_session.client('bedrock-runtime'),
            model_id=self.model_id,
            model_kwargs=model_kwargs
        )

    def run(self, prompt):
            if self.model_instance is None:
                raise ValueError("Model instance is not initialized. Call the 'build' method first.")

            prompt = "\n".join(f"{role}: {content}" for role, content in prompt)
            human_message = HumanMessage(content=prompt)

            response = self.model_instance.invoke([human_message])
            return response.content
