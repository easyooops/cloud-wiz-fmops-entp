from typing import Dict, Union  
from loguru import logger  
from uuid import UUID 
from app.core.interface.service import NoFactoryRegisteredError, ServiceFactory, ServiceType, StorageService  
from app.core.provider.database.SQLAlchemy import SQLAlchemyServiceFactory
from app.core.provider.database.MySQL import MySQLServiceFactory
from app.core.provider.database.SQLite import SQLiteServiceFactory
from app.core.provider.storage.S3 import S3StorageServiceFactory  
from app.core.provider.storage.AzureStorage import AzureStorageServiceFactory
from app.core.provider.storage.GCS import GCSStorageServiceFactory  
  
class ServiceManager:  
    def __init__(self):  
        self.services: Dict[str, Union[StorageService]] = {}  
        self.factories: Dict[ServiceType, ServiceFactory] = self._initialize_factories()  
  
    def _initialize_factories(self) -> Dict[ServiceType, ServiceFactory]:  
        return {
            ServiceType.SQLALCHEMY: SQLAlchemyServiceFactory(),
            ServiceType.MYSQL: MySQLServiceFactory(),
            ServiceType.SQLITE: SQLiteServiceFactory(),
        } 
  
    def register_factory(self, service_type: ServiceType, factory: ServiceFactory):  
        self.factories[service_type] = factory  
  
    def get_service(self, service_type: ServiceType, config: dict = None) -> Union[StorageService]:  
        if service_type not in self.services:  
            self._create_service(service_type, config)  
        return self.services[service_type.value]  
  
    def _create_service(self, service_type: ServiceType, config: dict = None):  
        if config:  
            if service_type == ServiceType.S3:  
                factory = S3StorageServiceFactory(  
                    aws_access_key_id=config['aws_access_key_id'],  
                    aws_secret_access_key=config['aws_secret_access_key'],  
                    aws_region=config['aws_region'],  
                    bucket_name=config['bucket_name']  
                )  
            elif service_type == ServiceType.AZURE_STORAGE:  
                factory = AzureStorageServiceFactory(  
                    account_name=config['account_name'],  
                    account_key=config['account_key'],  
                    container_name=config['container_name'],  
                    sas_token=config['sas_token']  
                )  
            elif service_type == ServiceType.GCS:  
                factory = GCSStorageServiceFactory(  
                    project_id=config['project_id'],  
                    bucket_name=config['bucket_name'],  
                    credentials_json=config['credentials_json']  
                )  
            else:  
                raise ValueError(f"Unsupported service type: {service_type}")  
            self.register_factory(service_type, factory)  
  
        factory = self.factories.get(service_type)  
        if not factory:  
            raise NoFactoryRegisteredError(f"No factory registered for {service_type.name}")  
        self.services[service_type.value] = factory.create()  
        self.services[service_type.value].set_ready()  
  
    def teardown_services(self):  
        for service in self.services.values():  
            if service:  
                logger.debug(f"Teardown service {service.__class__.__name__}")  
                service.teardown()  
        self.services = {}