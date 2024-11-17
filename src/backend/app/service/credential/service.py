import json
import logging
import os
from typing import List, Optional
from sqlalchemy import func
from sqlmodel import Session, desc, select
from uuid import UUID

from app.service.credential.model import Credential
from app.api.v1.schemas.credential import CredentialCreate, CredentialProviderJoin, CredentialUpdate
from app.service.provider.model import Provider
from app.service.agent.model import Agent
from app.core.interface.service import ServiceType, StorageService
from app.core.manager import ServiceManager
from app.service.auth.service import AuthService
from app.components.DocumentLoader.Notion import NotionDocumentLoader
from app.components.DocumentLoader.Snowflake import SnowflakeDocumentLoader
from app.components.DocumentLoader.GIT import GitDocumentLoader

class CredentialService():
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.service_manager = ServiceManager()
        self.store_bucket = os.getenv("AWS_S3_BUCKET_STORE_NAME")
    
    def get_all_credentials(self, user_id: Optional[UUID] = None, credential_id: Optional[UUID] = None, provider_id: Optional[UUID] = None) -> List[CredentialProviderJoin]:
        statement = select(Credential, Provider).join(Provider, Credential.provider_id == Provider.provider_id)
        if user_id:
            statement = statement.where(Credential.user_id == user_id)
        if credential_id:
            statement = statement.where(Credential.credential_id == credential_id)
        if provider_id:
            statement = statement.where(Credential.provider_id == provider_id)
                    
        statement = statement.order_by(desc(Credential.credential_id))
                            
        results = self.session.execute(statement).all()

        credentials = []
        for credential, provider in results:
            expected_count = self._calculate_expected_count(user_id, provider, credential)
            credentials.append(self._map_to_credential_out(credential, provider, expected_count))
        
        return credentials

    def _calculate_expected_count(self, user_id: UUID, provider: Provider, credential: Credential) -> int:
        result = 0

        if provider.type == 'M':
            agent_statement = select(func.sum(Agent.expected_token_count)).where(
                Agent.user_id == user_id
            )            
            agent_statement = agent_statement.where(Agent.fm_provider_id == provider.provider_id)
            result = self.session.execute(agent_statement).scalar() or 0
        elif provider.type == 'S':
            full_directory_name = f"{user_id}"
            try:
                # 스토리지 서비스 가져오기
                storage_service = self._set_storage_credential(credential_id=credential.credential_id)
                if storage_service:
                    # 스토리지 서비스 사용
                    result = storage_service.get_directory_info(full_directory_name)['total_size']
                else:
                    result = 0
            except Exception as e:
                print(f"Error while getting storage information: {e}")
                result = 0
        elif provider.type == 'V':
            result = 0

        return result
        
    def mask_sensitive_data(self, data: Optional[str]) -> Optional[str]:
        if data is None or len(data) <= 4:
            return data
        return data[:2] + '*' * 10 + data[-2:]
    
    def _map_to_credential_out(self, credential: Credential, provider: Provider, expected_count: int) -> CredentialProviderJoin:
        return CredentialProviderJoin(
            credential_id=credential.credential_id,
            user_id=credential.user_id,
            provider_id=credential.provider_id,
            credential_name=credential.credential_name,
            access_key=self.mask_sensitive_data(credential.access_key),
            secret_key=self.mask_sensitive_data(credential.secret_key),
            session_key=self.mask_sensitive_data(credential.session_key),
            access_token=self.mask_sensitive_data(credential.access_token),
            api_key=self.mask_sensitive_data(credential.api_key),
            api_endpoint=credential.api_endpoint,
            git_clone_url=credential.git_clone_url,
            git_branch=credential.git_branch,
            git_repo_path=credential.git_repo_path,
            git_file_filter=credential.git_file_filter,
            db_user=self.mask_sensitive_data(credential.db_user),
            db_password="***********",
            db_account=self.mask_sensitive_data(credential.db_account),
            db_role=self.mask_sensitive_data(credential.db_role),
            db_database=self.mask_sensitive_data(credential.db_database),
            db_schema=self.mask_sensitive_data(credential.db_schema),
            db_warehouse=self.mask_sensitive_data(credential.db_warehouse),
            db_query=credential.db_query,
            inner_used=credential.inner_used,
            limit_cnt=credential.limit_cnt,
            provider_name=provider.name,
            provider_company=provider.company,
            provider_key=provider.pvd_key,
            provider_desc=provider.description,
            provider_logo=provider.logo,
            provider_type=provider.type,
            provider_ord=provider.sort_order,
            expected_count=expected_count  
        )
    
    def create_credential(self, credential_data: CredentialCreate):
        try:
            new_credential = Credential(**credential_data.model_dump())
            self.session.add(new_credential)
            self.session.commit()
            self.session.refresh(new_credential)
            return new_credential
        except Exception as e:
            raise e

    def update_credential(self, credential_id: UUID, credential_update: CredentialUpdate):
        try:
            credential = self.session.get(Credential, credential_id)
            for key, value in credential_update.model_dump(exclude_unset=True).items():
                setattr(credential, key, value)
            self.session.add(credential)
            self.session.commit()
            self.session.refresh(credential)
            return credential
        except Exception as e:
            raise e

    def delete_credential(self, credential_id: UUID):
        try:
            credential = self.session.get(Credential, credential_id)
            self.session.delete(credential)
            self.session.commit()
        except Exception as e:
            raise e

    def _set_storage_credential(self, credential_id: UUID) -> StorageService:
        try:
            credential_query = (
                select(Credential, Provider)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
            )
            result = self.session.execute(credential_query).first()

            if not result:
                raise ValueError(f"Credential with id {credential_id} and provider type 'S' not found")

            credential, provider = result

            aws = AuthService.get_aws_key()

            if credential.inner_used:
                config = {
                    'aws_access_key_id': aws['aws_access_key'],
                    'aws_secret_access_key': aws['aws_secret_access_key'],
                    'aws_region': aws['aws_region'],
                    'bucket_name': self.store_bucket,
                    'credentials_json': os.getenv('GOOGLE_DRIVE_CREDENTIALS_JSON'),
                    'api_token': os.getenv('NOTION_API_TOKEN'),
                    'database_id': os.getenv('NOTION_DATABASE_ID'),
                    'token': os.getenv('GITHUB_TOKEN'),
                    'repo': os.getenv('GITHUB_REPO'),
                    'owner': os.getenv('GITHUB_OWNER'),
                    'access_token': os.getenv('ACCESS_TOKEN'),
                    'refresh_token': os.getenv('REFRESH_TOKEN')
                }
            else:
                config = {
                    'aws_access_key_id': credential.access_key,
                    'aws_secret_access_key': credential.secret_key,
                    'aws_region': aws['aws_region'],
                    'bucket_name': self.store_bucket,
                    'credentials_json': credential.api_key,
                    'api_token': credential.access_token,
                    'database_id': credential.api_endpoint,
                    'token': credential.access_token,
                    'repo': credential.session_key,
                    'owner': credential.secret_key,
                    'access_token': credential.access_token,
                    'refresh_token': credential.refresh_token
                }

            if provider.pvd_key == "AS":
                return self.service_manager.get_service(ServiceType.S3, config)
            elif provider.pvd_key == "GD":
                return self.service_manager.get_service(ServiceType.GOOGLE_DRIVE, config)
            elif provider.pvd_key == "NT":
                return self.service_manager.get_service(ServiceType.NOTION, config)
            elif provider.pvd_key == "GH":
                return self.service_manager.get_service(ServiceType.GITHUB, config)
            else:
                raise ValueError(f"Unsupported provider key: {provider.pvd_key}")
            
        except Exception as e:
            print(f"Error while setting storage credential: {e}")
            return None

    def _set_document_loader_credential(self, credential_id: UUID):
        try:
            credential_query = (
                select(Credential, Provider)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
                .where(Provider.type == "L")
            )
            result = self.session.execute(credential_query).first()

            if not result:
                raise ValueError(f"Credential with id {credential_id} and provider type 'S' not found")

            credential, provider = result

            config = {
                'git_clone_url': credential.git_clone_url,
                'git_branch': credential.git_branch,
                'git_repo_path': credential.git_repo_path,
                'git_file_filter': credential.git_file_filter,
                'api_token': credential.access_token,
                'db_query': credential.db_query,
                'db_user': credential.db_user,
                'db_password': credential.db_password,
                'db_account': credential.db_account,
                'db_warehouse': credential.db_warehouse,
                'db_role': credential.db_role,
                'db_database': credential.db_database,
                'db_schema': credential.db_schema
            }

            if provider.pvd_key == "SF":
                return SnowflakeDocumentLoader(config=config)
            elif provider.pvd_key == "NT":
                return NotionDocumentLoader(config=config)
            elif provider.pvd_key == "GH":
                return GitDocumentLoader(config=config)
            else:
                raise ValueError(f"Unsupported provider key: {provider.pvd_key}")

        except Exception as e:
            print(f"Error while setting document loader credential: {e}")
            raise