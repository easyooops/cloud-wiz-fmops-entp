import json
import logging
from pathlib import Path
from uuid import UUID
from sqlmodel import Session, select, delete
from app.service.store.service import StoreService
from app.api.v1.schemas.store import StoreCreate
from app.service.credential.model import Credential
from app.service.processing.model import Processing
from app.service.agent.model import Agent
from app.service.store.model import Store
from app.service.provider.model import Provider
from app.service.model.model import Model

class InitDataService:

    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    def load_json_data(self, file_path):
        data_path = Path(file_path)
        return json.loads(data_path.read_text())

    def create_credential_data(self, credential_data):
        # self.clear_credential_table()
        credentials = []
        for data in credential_data:
            pvd_key = data.pop("pvd_key")
            provider = self.session.execute(select(Provider).where(Provider.pvd_key == pvd_key)).first()

            if provider:
                provider_id = provider[0].provider_id
            else:
                provider_id = None  # 예외 처리 필요

            data["provider_id"] = provider_id
            data["credential_name"] = 'Default ' + provider[0].name
            data["creator_id"] = self.user_id
            data["updater_id"] = self.user_id
            data["user_id"] = self.user_id

            credentials.append(Credential(**data))

        self.session.add_all(credentials)
        self.session.commit()

    def create_store_data(self):
        # self.clear_store_table()

        store_provider = self.session.execute(
                select(Credential)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Provider.pvd_key == "AS")
            ).first()
        store_provider_id = store_provider[0].credential_id

        vector_store_provider = self.session.execute(
                select(Credential)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Provider.pvd_key == "CM")
            ).first()
        vector_store_provider_id = vector_store_provider[0].credential_id

        store_data = StoreCreate(
            store_name="Default Storage",
            description="Default Storage with Cloudwiz AI FMOps",
            creator_id=self.user_id,
            updater_id=self.user_id,
            credential_id=store_provider_id,
            user_id=self.user_id
        )

        service = StoreService(self.session)
        service.create_store(store_data, self.user_id)

    def create_processing_data(self, processing_data):
        # self.clear_processing_table()
        processings = []
        for data in processing_data:
            data["creator_id"] = self.user_id
            data["updater_id"] = self.user_id
            data["user_id"] = self.user_id

            processings.append(Processing(**data))

        self.session.add_all(processings)
        self.session.commit()

    def create_agent_data(self, agent_data):
        # self.clear_agent_table()
        agents = []
        for data in agent_data:
            fm_provider = self.session.execute(
                    select(Credential)
                    .join(Provider, Credential.provider_id == Provider.provider_id)
                    .where(Provider.pvd_key == "OA")
                ).first()
            fm_provider_id = fm_provider[0].credential_id
            if not self.validate_uuid(fm_provider_id):
                continue

            data["fm_provider_id"] = fm_provider_id
            data["embedding_provider_id"] = fm_provider_id

            model_typ = data.pop("fm_provider_type")
            model_name = None
            if model_typ == "C":
                model_name = "gpt-3.5-turbo"
            elif model_typ == "T":
                model_name = "gpt-3.5-turbo-instruct"

            fm_model = self.session.execute(select(Model).where(Model.model_name == model_name)).first()
            fm_model_id = fm_model[0].model_id
            if not self.validate_uuid(fm_model_id):
                continue

            data["fm_provider_type"] = model_typ
            data["fm_model_id"] = fm_model_id

            embedding_model = self.session.execute(select(Model).where(Model.model_name == "text-embedding-ada-002")).first()
            embedding_model_id = embedding_model[0].model_id
            if not self.validate_uuid(embedding_model_id):
                continue

            data["embedding_model_id"] = embedding_model_id

            store_provider = self.session.execute(
                    select(Credential)
                    .join(Provider, Credential.provider_id == Provider.provider_id)
                    .where(Provider.pvd_key == "AS")
                ).first()
            store_provider_id = store_provider[0].credential_id

            if not self.validate_uuid(store_provider_id):
                continue

            data["storage_provider_id"] = store_provider_id

            object_name = self.session.execute(select(Store).where(Store.store_name == "Default Storage")).first()
            object_name_id = object_name[0].store_id        
            if not self.validate_uuid(object_name_id):
                continue

            data["storage_object_id"] = object_name_id

            pre_processing = self.session.execute(select(Processing).where(Processing.processing_type == "pre")).first()
            pre_processing_id = pre_processing[0].processing_id
            if not self.validate_uuid(pre_processing_id):
                continue

            data["pre_processing_id"] = pre_processing_id

            post_processing = self.session.execute(select(Processing).where(Processing.processing_type == "post")).first()
            post_processing_id = post_processing[0].processing_id
            if not self.validate_uuid(post_processing_id):
                continue

            data["post_processing_id"] = post_processing_id

            data["vector_db_provider_id"] = None
            data["creator_id"] = self.user_id
            data["updater_id"] = self.user_id
            data["user_id"] = self.user_id

            agents.append(Agent(**data))

        self.session.add_all(agents)
        self.session.commit()

    def clear_credential_table(self):
        statement = delete(Credential)
        self.session.execute(statement)
        self.session.commit()

    def clear_store_table(self):
        service = StoreService(self.session)
        statement = select(Store)
        stores = self.session.execute(statement).all()
        for store in stores:
            service.delete_store(store.store_id)

    def clear_processing_table(self):
        statement = delete(Processing)
        self.session.execute(statement)
        self.session.commit()

    def clear_agent_table(self):
        statement = delete(Agent)
        self.session.execute(statement)
        self.session.commit()

    def validate_uuid(self, value):
        if isinstance(value, UUID):
            return True
        try:
            uuid_obj = UUID(value)
            return True
        except ValueError:
            return False

    def run(self):
        credential_data = self.load_json_data("./app/data/credential_data.json")
        processing_data = self.load_json_data("./app/data/processing_data.json")
        agent_data = self.load_json_data("./app/data/agent_data.json")
        
        self.create_credential_data(credential_data)
        self.create_store_data()
        self.create_processing_data(processing_data)
        self.create_agent_data(agent_data)


