import json
from pathlib import Path
import uuid
from sqlmodel import Session, select, delete
from uuid import UUID

from app.service.provider.model import Provider
from app.service.model.model import Model
from app.service.credential.model import Credential
from app.service.store.model import Store
from app.service.store.service import StoreService
from app.api.v1.schemas.store import StoreCreate
from app.service.processing.model import Processing
from app.service.agent.model import Agent


def init_db(session: Session):
    provider_data_path = Path("./app/data/provider_data.json")
    model_data_path = Path("./app/data/model_data.json")

    provider_data = json.loads(provider_data_path.read_text())
    model_data = json.loads(model_data_path.read_text())

    clear_provider_table(session)

    statement = select(Provider)
    results = session.exec(statement)
    if not results.first():
        for data in provider_data:
            data['provider_id'] = uuid.uuid4()
            data['creator_id'] = ensure_uuid(data['creator_id'])
            if data.get('updater_id'):
                data['updater_id'] = ensure_uuid(data['updater_id'])
        providers = [Provider(**data) for data in provider_data]
        session.add_all(providers)
        session.commit()

    create_model_data(session, model_data)

def clear_provider_table(session: Session):
    statement = delete(Provider)
    session.exec(statement)
    session.commit()

def create_model_data(session: Session, model_data):

    clear_model_table(session)
    models = []
    for data in model_data:
        pvd_key = data.pop("pvd_key")
        provider = session.exec(select(Provider).where(Provider.pvd_key == pvd_key)).first()
        if provider:
            provider_id = provider.provider_id

        data["provider_id"] = provider_id
        data['creator_id'] = ensure_uuid(data['creator_id'])
        if data.get('updater_id'):
            data['updater_id'] = ensure_uuid(data['updater_id'])
        models.append(Model(**data))

    session.add_all(models)
    session.commit()

def clear_model_table(session: Session):
    statement = delete(Model)
    session.exec(statement)
    session.commit()

def validate_uuid(value):
    if isinstance(value, uuid.UUID):
        return True
    try:
        uuid_obj = uuid.UUID(value)
        return True
    except ValueError:
        return False  
    

def ensure_uuid(value):
    if isinstance(value, str):
        return UUID(value)
    return value    