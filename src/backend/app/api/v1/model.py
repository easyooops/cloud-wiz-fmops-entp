from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.service.model.service import (
    ModelService, OpenAIService, OllamaService, AnthropicService,
    AL21LabsService, CohereService, TitanService
)
from app.core.exception import internal_server_error
from app.service.model.model import Model
from app.api.v1.schemas.model import ModelCreate, ModelUpdate
from app.core.factories import get_database
from app.service.auth.service import get_current_user

router = APIRouter()

SERVICE_CLASSES = {
    "openai": OpenAIService,
    "ollama": OllamaService,
    "anthropic": AnthropicService,
    "al21labs": AL21LabsService,
    "cohere": CohereService,
    "titan": TitanService
}

@router.get("/{model_name}/models")
def get_models(
    model_name: str,
    token: str = Depends(get_current_user) 
):
    try:
        service_class = SERVICE_CLASSES.get(model_name.lower())
        if not service_class:
            raise HTTPException(status_code=400, detail="Invalid model name")
        
        service = service_class()
        return service.get_models()
    except Exception as e:
        raise internal_server_error(e)

@router.get("/", response_model=List[Model])
def get_models(
    provider_id: Optional[UUID] = None,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ModelService(session)
        return service.get_all_models(provider_id)
    except Exception as e:
        raise internal_server_error(e)

# POST
@router.post("/", response_model=Model)
def create_model(
    model: ModelCreate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ModelService(session)
        return service.create_model(model)
    except Exception as e:
        raise internal_server_error(e)

# PUT
@router.put("/{model_id}", response_model=Model)
def update_model(
    model_id: UUID,
    model: ModelUpdate,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ModelService(session)
        return service.update_model(model_id, model)
    except Exception as e:
        raise internal_server_error(e)

# DELETE
@router.delete("/{model_id}", response_model=Model)
def delete_model(
    model_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = ModelService(session)
        return service.delete_model(model_id)
    except Exception as e:
        raise internal_server_error(e)