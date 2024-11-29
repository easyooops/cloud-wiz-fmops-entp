import json
from pathlib import Path  
from uuid import UUID  
from sqlmodel import Session, select, delete  
from app.service.store.service import StoreService  
from app.api.v1.schemas.store import StoreCreate  
from app.service.credential.model import Credential
from app.service.store.model import Store  
from app.service.provider.model import Provider  
import os  
  
class InitDataService:  
    def __init__(self, session: Session, user_id: str):  
        self.session = session  
        self.user_id = user_id  
        self.csp_provider = os.getenv('CSP_PROVIDER')  # 환경변수 가져오기  
  
    def load_json_data(self, file_path):  
        data_path = Path(file_path)  
        return json.loads(data_path.read_text())  
  
    def create_credential_data(self):
        credentials = []  
        providers = self.session.execute(select(Provider).where(Provider.pvd_key == self.csp_provider)).all()  
  
        for provider in providers:  
            provider_id = provider[0].provider_id  
            data = {  
                "provider_id": provider_id,  
                "credential_name": provider[0].name,  
                "creator_id": self.user_id,  
                "updater_id": self.user_id,  
                "user_id": self.user_id  
            }  
            credentials.append(Credential(**data))  
  
        self.session.add_all(credentials)  
        self.session.commit()  
  
    def create_store_data(self):  
        store_provider = self.session.execute(  
            select(Credential)  
            .join(Provider, Credential.provider_id == Provider.provider_id)  
            .where(Provider.pvd_key == self.csp_provider, Provider.type == 'S')  
        ).first()  
        
        if store_provider is None:  
            raise ValueError("No store provider found matching the criteria.")  
    
        store_provider_id = store_provider[0].credential_id  
    
        store_data = StoreCreate(  
            store_name="기본 저장소",  
            description="기본 저장소로 문서 업로드시 즉시 백터 임베딩을 수행합니다.",  
            creator_id=self.user_id,  
            updater_id=self.user_id,  
            credential_id=store_provider_id,  
            user_id=self.user_id  
        )  
    
        service = StoreService(self.session)  
        service.create_store(store_data, self.user_id)  
  
    def validate_uuid(self, value):  
        if isinstance(value, UUID):  
            return True  
        try:  
            uuid_obj = UUID(value)  
            return True  
        except ValueError:  
            return False  
  
    def run(self):
        self.create_credential_data()  
        self.create_store_data() 