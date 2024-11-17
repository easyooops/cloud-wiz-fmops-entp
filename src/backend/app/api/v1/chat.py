import json
import os
from dotenv import load_dotenv
from typing import Optional
from fastapi import APIRouter, Depends

from app.core.exception import internal_server_error
from app.api.v1.schemas.chat import ChatResponse
from app.components.LLM.OpenAI import OpenAILLMComponent
from app.components.LLM.Ollama import OllamaLLMComponent
from app.components.LLM.Bedrock import BedrockLLMComponent
from app.service.auth.service import AuthService, get_current_user

router = APIRouter()
load_dotenv()

@router.get("/llms-openai", response_model=ChatResponse)
def get_llm_openai_answer(
    query: Optional[str] = None,
    model_id: Optional[str] = None,
    temperature: Optional[float] = 0.9,
    top_p: Optional[float] = 0,
    max_tokens: Optional[int] = 250,
    token: str = Depends(get_current_user)     
):
    try:
        openai_api_key = AuthService.get_openai_key()
                
        openai_component = OpenAILLMComponent(openai_api_key)
        openai_component.build(
                model_id=model_id,
                temperature=temperature,
                top_p=top_p,
                max_tokens=max_tokens
            )

        return ChatResponse(answer=openai_component.run(query))
    except Exception as e:
        raise internal_server_error(e)

@router.get("/llms-ollama", response_model=ChatResponse)
def get_llm_ollama_answer(
    query: Optional[str] = None,
    token: str = Depends(get_current_user) 
):
    try:
        ollama_component = OllamaLLMComponent()
        ollama_component.build()

        return ChatResponse(answer=ollama_component.run(query))
    except Exception as e:
        raise internal_server_error(e)
    
@router.get("/llms-bedrock", response_model=ChatResponse)
def get_llm_bedrock_answer(
    model: str = None,
    query: Optional[str] = None,
    token: str = Depends(get_current_user) 
):
    try:
        # model = "amazon.titan-text-express-v1"
        bedrock_component = BedrockLLMComponent(model)
        bedrock_component.build()

        return ChatResponse(answer=bedrock_component.run(query))
    except Exception as e:
        raise internal_server_error(e)    