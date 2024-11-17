import logging
import boto3
import tiktoken
from tokencost import calculate_prompt_cost, count_string_tokens, calculate_completion_cost
from langchain_aws import ChatBedrock
from langchain_openai import ChatOpenAI

class TokenUtilityService:
    def __init__(self, aws_access_key, aws_secret_access_key, aws_region):
        super().__init__()
        self.aws_access_key = aws_access_key
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region

        if(self.aws_access_key and self.aws_secret_access_key and self.aws_region):
            self.boto3_session = boto3.Session(
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
            self.bedrock_client = self.boto3_session.client('bedrock-runtime')

    def get_bedrock_token_count(self, text, model_id):
        try:
            # llm = ChatBedrock(model_id=model_id)
            # response = llm.invoke([("human", text)])

            # response = self.bedrock_client.invoke_model(
            #     modelId=model_id,
            #     Body=text,
            #     ContentType='application/json',
            #     Accept='application/json'
            # )
            tokens = 0
            # if response['usage']['total_tokens']:
            #     tokens = int(response.response_metadata['usage']['total_tokens'])


            # response_metadata = response.response_metadata  # AIMessage 객체의 usage_metadata

            # if response_metadata:
            #     usage = response_metadata.get('usage')
            #     if usage:
            #         total_tokens = usage.get('total_tokens')
            #         if isinstance(total_tokens, int):
            #             tokens = total_tokens
            #         else:
            #             # total_tokens가 int 형식이 아닌 경우 처리
            #             logging.warning(f"total_tokens is not an integer: {total_tokens}")
            # else:
            #     # usage_metadata가 없는 경우 처리
            #     logging.warning("usage_metadata is not available: {usage_metadata}")  
            return tokens
        
        except Exception as e:
            print(f"Error calculating Bedrock token count: {e}")
            return None

    def get_openai_token_count(self, text, model_id):
        try:
            encoding = tiktoken.encoding_for_model(model_id)
            tokens = encoding.encode(text)
            return len(tokens)
        except Exception as e:
            print(f"Error get_openai_token_count: {e}")
            return None
        
    def get_token_count(self, text, model_id):
        try:
            return count_string_tokens(prompt=text, model=model_id)
        except Exception as e:
            print(f"Error get_token_count: {e}")
            return None
        
    def get_prompt_cost(self, text, model_id):
        try:
            return calculate_prompt_cost(prompt=text, model=model_id)
        except Exception as e:
            print(f"Error get_prompt_cost: {e}")
            return None
        
    def get_completion_cost(self, text, model_id):
        try:
            return calculate_completion_cost(completion=text, model=model_id)
        except Exception as e:
            print(f"Error get_completion_cost: {e}")
            return None        