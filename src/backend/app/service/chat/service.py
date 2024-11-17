import json
import os
from fastapi import HTTPException
from sqlmodel import Session
from typing import Optional
from app.components.Chat.OpenAI import ChatOpenAIComponent
from app.components.Chat.Bedrock import ChatBedrockComponent
from app.components.Chat.QueryTuning import QueryTuningComponent
from app.service.auth.service import AuthService

class ChatService:
    def __init__(self, session: Session):
        self.session = session

    def get_llm_openai_instance(self, model_id: str, max_tokens: int = 150, temperature: float = 0.7):
        try:
            openai_api_key = AuthService.get_openai_key()
            
            if not openai_api_key:
                raise ValueError("OpenAI API key is not set in the environment variables")

            openai_component = ChatOpenAIComponent(openai_api_key)
            openai_component.build(model_id=model_id, max_tokens=max_tokens, temperature=temperature)
            return openai_component.model_instance
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_llm_openai_response(self, query: str):
        llm = self.get_llm_openai_instance(model_id="gpt-3.5-turbo", max_tokens=500, temperature=0.7)
        return llm({"input": query})

    def get_llm_bedrock_instance(self, model_id: str, max_tokens: int = 150, temperature: float = 0.7):
        try:
            aws = AuthService.get_aws_key()
            aws_access_key = aws['aws_access_key']
            aws_secret_access_key = aws['aws_secret_access_key']
            aws_region = aws['aws_region']

            if not all([aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("AWS credentials or region are not set in the environment variables")

            bedrock_component = ChatBedrockComponent(
                aws_access_key=aws_access_key,
                aws_secret_access_key=aws_secret_access_key,
                aws_region=aws_region
            )
            bedrock_component.build(model_id=model_id, max_tokens=max_tokens, temperature=temperature)
            return bedrock_component.model_instance
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def get_llm_bedrock_response(self, query: str):
        llm = self.get_llm_bedrock_instance(model_id="anthropic.claude-3-sonnet-20240229-v1:0", max_tokens=500, temperature=0.7)
        return llm({"input": query})


    # QueryTuning (OpenAI + Bedrock)
    def openai_chaining(self, query: str, model_id: str, service_type: str = "openai", max_tokens: int = 150, temperature: float = 0.7):
        try:
            openai_api_key = AuthService.get_openai_key()

            aws = AuthService.get_aws_key()
            aws_access_key = aws['aws_access_key']
            aws_secret_access_key = aws['aws_secret_access_key']
            aws_region = aws['aws_region']

            if not all([openai_api_key, aws_access_key, aws_secret_access_key, aws_region]):
                raise ValueError("API keys or AWS credentials are not set in the environment variables")

            # 쿼리 유형 감지 및 전처리
            refinement_component = QueryTuningComponent(openai_api_key)
            refinement_component.build()
            refined_query = refinement_component.run(query)

            # 서비스 유형에 따른 컴포넌트 선택
            if service_type == "bedrock":
                bedrock_component = ChatBedrockComponent()
                bedrock_component.build(model_id=model_id)
                response = bedrock_component.run(refined_query)
            else:
                openai_component = ChatOpenAIComponent(openai_api_key)
                openai_component.build(model_id=model_id, max_tokens=max_tokens, temperature=temperature)
                response = openai_component.run(refined_query)

            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))