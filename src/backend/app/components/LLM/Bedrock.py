import boto3

from langchain_aws import BedrockLLM
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

from app.components.LLM.Base import BaseLLMComponent

class BedrockLLMComponent(BaseLLMComponent):
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
            model_id="amazon.titan-text-lite-v1"

        model_kwargs = {"temperature": temperature, "top_p": top_p, "max_tokens": max_tokens}

        if "ai21" in model_id:
            del model_kwargs["top_p"]
            del model_kwargs["max_tokens"]

        if "cohere" in model_id:
            del model_kwargs["top_p"]

        if "amazon" in model_id:
            del model_kwargs["top_p"]
            del model_kwargs["max_tokens"]

        if "meta" in model_id:
            del model_kwargs["max_tokens"]

        llm = BedrockLLM(
            client=self.boto3_session.client('bedrock-runtime'),
            model_id=model_id,
            model_kwargs=model_kwargs
        )        
        self.conversation = ConversationChain(
            llm=llm, verbose=True, memory=ConversationBufferMemory()
        )
        self.model_instance = llm

    def run(self, prompt):
        if self.conversation is None:
            raise ValueError("LLM is not initialized. Call the build method first.")
        return self.conversation.predict(input=prompt)