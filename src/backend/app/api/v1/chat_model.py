import os
from http.client import HTTPException
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing import Optional

from app.core.factories import get_database
from app.core.exception import internal_server_error
from app.api.v1.schemas.chat import ChatResponse
from app.service.chat.service import ChatService
from app.service.auth.service import get_current_user

router = APIRouter()
load_dotenv()

# OpenAI
@router.post("/chat-openai", response_model=ChatResponse)
def get_openai_chat_answer(
    query: Optional[str] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        chat_service = ChatService(session)
        response = chat_service.get_llm_openai_response(query)
        return ChatResponse(answer=response)
    except Exception as e:
        raise internal_server_error(e)

# Bedrock
@router.post("/chat-bedrock", response_model=ChatResponse)
def get_bedrock_chat_answer(
    query: Optional[str] = None,
    model: str = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        if not query or not model:
            raise HTTPException(status_code=400, detail="Query and model parameters are required")

        chat_service = ChatService(session)
        response = chat_service.get_llm_bedrock_response(model, query)
        return ChatResponse(answer=response)
    except Exception as e:
        raise internal_server_error(e)

# OpenAI + Bedrock Chaining
@router.post("/chat-chaining", response_model=ChatResponse)
def get_openai_bedrock_chaining(
    query: Optional[str] = None,
    model: str = None,
    service_type: str = "openai",
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user)
):
    try:
        if not query:
            raise HTTPException(status_code=400, detail="Query parameter is required")

        chat_service = ChatService(session)
        response = chat_service.openai_chaining(query, model_id=model, service_type=service_type)
        return ChatResponse(answer=response)
    except Exception as e:
        raise internal_server_error(e)