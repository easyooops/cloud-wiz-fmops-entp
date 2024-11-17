from uuid import UUID
from fastapi import HTTPException
import openai
import os
import requests
from typing import List, Optional
from dotenv import load_dotenv
from sqlmodel import Session, select

from app.api.v1.schemas.model import ModelCreate, ModelUpdate
from app.service.model.model import Model
from app.service.auth.service import AuthService

load_dotenv()

class ModelService:
    def __init__(self, session: Session):
        self.session = session

    def get_all_models(self, provider_id: Optional[UUID] = None) -> List[Model]:
        statement = select(Model)
        if provider_id:
            statement = statement.where(Model.provider_id == provider_id)
        return self.session.execute(statement).scalars().all()

    def create_model(self, model_create: ModelCreate) -> Model:
        model = Model.model_validate(model_create)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def update_model(self, model_id: UUID, model_update: ModelUpdate) -> Model:
        model = self.session.get(Model, model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        for key, value in model_update.dict(exclude_unset=True).items():
            setattr(model, key, value)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return model

    def delete_model(self, model_id: UUID) -> Model:
        model = self.session.get(Model, model_id)
        if not model:
            raise HTTPException(status_code=404, detail="Model not found")
        self.session.delete(model)
        self.session.commit()
        return model
    
class BaseModelService:
    def __init__(self, api_key: str, api_endpoint: str):
        self.api_key = api_key
        self.api_endpoint = api_endpoint

    def _get_headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _fetch_models(self) -> Optional[dict]:
        response = requests.get(self.api_endpoint, headers=self._get_headers())
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch models: {response.status_code}")

class OpenAIService(BaseModelService):
    def __init__(self):
        openai_api_key = AuthService.get_openai_key()
        super().__init__(api_key=openai_api_key, api_endpoint=os.getenv("OPENAI_API_ENDPOINT"))

    def get_models(self):
        openai.api_key = self.api_key
        response = openai.models.list()
        return list(response)

class OllamaService(BaseModelService):
    def __init__(self):
        super().__init__(api_key=os.getenv("OLLAMA_API_KEY"), api_endpoint=os.getenv("OLLAMA_API_ENDPOINT"))

    def get_models(self):
        return self._fetch_models()

class AnthropicService(BaseModelService):
    def __init__(self):
        super().__init__(api_key=os.getenv("ANTHROPIC_API_KEY"), api_endpoint=os.getenv("ANTHROPIC_API_ENDPOINT"))

    def get_models(self):
        return self._fetch_models()

class AL21LabsService(BaseModelService):
    def __init__(self):
        super().__init__(api_key=os.getenv("AL21LABS_API_KEY"), api_endpoint=os.getenv("AL21LABS_API_ENDPOINT"))

    def get_models(self):
        return self._fetch_models()

class CohereService(BaseModelService):
    def __init__(self):
        super().__init__(api_key=os.getenv("COHERE_API_KEY"), api_endpoint=os.getenv("COHERE_API_ENDPOINT"))

    def get_models(self):
        return self._fetch_models()

class TitanService(BaseModelService):
    def __init__(self):
        super().__init__(api_key=os.getenv("TITAN_API_KEY"), api_endpoint=os.getenv("TITAN_API_ENDPOINT"))

    def get_models(self):
        return self._fetch_models()