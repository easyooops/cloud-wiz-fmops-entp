import logging
import os
from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi import HTTPException, UploadFile
from sqlmodel import Session, desc, select
from app.service.store.model import Store
from app.api.v1.schemas.store import StoreCreate, StoreUpdate

from app.service.credential.model import Credential
from app.service.credential.service import CredentialService
from app.service.provider.model import Provider
from app.components.DocumentLoader.DocumentLoader import DocumentLoaderComponent

class StoreService():
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.credential_service = CredentialService(session)

    def get_all_stores(self, user_id: Optional[UUID] = None, store_id: Optional[UUID] = None):
        try:
            statement = select(Store)
            if user_id:
                statement = statement.where(Store.user_id == user_id)
            if store_id:
                statement = statement.where(Store.store_id == store_id)

            statement = statement.order_by(desc(Store.store_id))

            return self.session.execute(statement).scalars().all()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Error retrieving stores")

    def get_store_directory_info(self, user_id: UUID, directory_name: str, credential_id: UUID):
        try:
            full_directory_name = f"{user_id}/{directory_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=credential_id)
            if storage_service:
                return storage_service.get_directory_info(full_directory_name)
            else:
                print("Failed to initialize storage service")
                return {'total_size': 0, 'file_count': 0}
        except Exception as e:
            print(f"Error while retrieving directory info: {e}")
            return {'total_size': 0, 'file_count': 0}

    def create_store(self, store_data: StoreCreate, user_id: UUID):
        try:
            new_store = Store(**store_data.model_dump())
            self.session.add(new_store)
            self.session.commit()
            self.session.refresh(new_store)
            full_directory_name = f"{user_id}/{new_store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=new_store.credential_id)
            if storage_service:
                storage_service.retry(lambda: storage_service.create_directory(full_directory_name))
            else:
                print("Failed to initialize storage service")
            return new_store

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error creating store: {str(e)}")

    def update_store(self, store_id: UUID, store_update: StoreUpdate, user_id: UUID):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            for key, value in store_update.model_dump(exclude_unset=True).items():
                setattr(store, key, value)
            self.session.add(store)
            self.session.commit()
            self.session.refresh(store)
            return store
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error updating store: {str(e)}")

    def delete_store(self, store_id: UUID, user_id: UUID):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            self.session.delete(store)
            self.session.commit()
            full_directory_name = f"{user_id}/{store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = os.getenv("CSP_PROVIDER")

            if provider_key in ["aws", "azure", "gcp"]:
                storage_service.delete_directory(full_directory_name)
            else:
                try:
                    store_folder_id = storage_service.get_folder_hierarchy_id(full_directory_name)
                    storage_service.delete_directory(store_folder_id)
                except FileNotFoundError:
                    logging.error(f"No folder found with the name: {full_directory_name}")
                    raise HTTPException(status_code=404, detail=f"No folder found with the name: {full_directory_name}")
        except HTTPException as e:
            raise e
        except Exception as e:
            logging.error(f"Error deleting store: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting store: {str(e)}")

    def list_files(self, user_id: UUID, store_id: UUID) -> List[Dict[str, Any]]:  
        try:  
            store = self.session.get(Store, store_id)  
            if not store:  
                raise HTTPException(status_code=404, detail="Store not found")  
            full_directory_name = f"{user_id}/{store.store_name}"  
            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)  
            if not storage_service:  
                logging.error("Failed to initialize storage service")  
                return []  
            provider_key = os.getenv("CSP_PROVIDER")  
            
            if provider_key in ["aws", "azure", "gcp"]:  
                objects = storage_service.list_all_objects(full_directory_name)  
            else:  
                parts = full_directory_name.split('/')  
                parent_id = None  
                for part in parts:  
                    try:  
                        parent_id = storage_service.get_folder_id_by_name(part)  
                    except FileNotFoundError:  
                        parent_id = storage_service.create_directory(part, parent_id)['id']  
                objects = storage_service.list_files_in_folder(parent_id)  
            
            files = []  
            if provider_key == "aws":  
                for obj in objects:  
                    file_info = {  
                        "Key": obj["Key"],  
                        "LastModified": obj["LastModified"],  
                        "Size": obj["Size"],  
                    }  
                    files.append(file_info)  
            elif provider_key == "azure":  
                for obj in objects: 
                    file_info = {  
                        "Key": obj["Key"],  
                        "LastModified": obj["LastModified"],  
                        "Size": obj["Size"],  
                    }  
                    files.append(file_info)  
            elif provider_key == "gcp":  
                for obj in objects:  
                    file_info = {  
                        "Key": obj["name"],  
                        "LastModified": obj["updated"],  
                        "Size": obj["size"],  
                    }  
                    files.append(file_info)  
            else:  
                for obj in objects:  
                    file_info = {  
                        "Key": obj.get("name") or obj.get("Name"),  
                        "LastModified": obj.get("modifiedTime", ""),  
                        "Size": obj.get("size", 0),  
                    }  
                    files.append(file_info)  
            
            logging.info(f"Files: {files}")  
            return files  
        except Exception as e:  
            logging.error(f"Error listing files: {str(e)}")  
            return []  

    def upload_file_to_store(self, user_id: UUID, store_id: UUID, file: UploadFile):
        tmp_path = None
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")
            folder_name = f"{user_id}/{store.store_name}"

            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = os.getenv("CSP_PROVIDER") 

            if provider_key in ["aws", "azure", "gcp"]:
                file_location = f"{folder_name}/{file.filename}"
                storage_service.upload_file(file.file, file_location)
            else:
                parts = folder_name.split('/')
                parent_id = None
                for part in parts:
                    try:
                        parent_id = storage_service.get_folder_id_by_name(part)
                    except FileNotFoundError:
                        parent_id = storage_service.create_directory(part, parent_id)['id']

                storage_service.upload_file_to_folder(parent_id, file)
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.remove(tmp_path)

    def delete_file_from_store(self, user_id: UUID, store_id: UUID, file_name: str):
        try:
            store = self.session.get(Store, store_id)
            if not store:
                raise HTTPException(status_code=404, detail="Store not found")

            full_directory_name = f"{user_id}/{store.store_name}"
            storage_service = self.credential_service._set_storage_credential(credential_id=store.credential_id)
            if not storage_service:
                logging.error("Failed to initialize storage service")
                raise HTTPException(status_code=500, detail="Failed to initialize storage service")

            provider_key = os.getenv("CSP_PROVIDER") 

            if provider_key in ["aws", "azure", "gcp"]:
                file_location = f"{full_directory_name}/{file_name}"
                storage_service.delete_file(file_location)
            else:
                parts = full_directory_name.split('/')
                parent_id = None
                for part in parts:
                    try:
                        parent_id = storage_service.get_folder_id_by_name(part)
                    except FileNotFoundError:
                        parent_id = storage_service.create_directory(part, parent_id)['id']
                try:
                    file_id = storage_service.get_file_id_by_name(parent_id, file_name)
                except FileNotFoundError:
                    logging.error(f"No file found with the name: {file_name} in folder: {full_directory_name}")
                    raise HTTPException(status_code=404, detail=f"No file found with the name: {file_name} in folder: {full_directory_name}")

                storage_service.delete_file(file_id)
        except Exception as e:
            logging.error(f"Error deleting file from store: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting file from store: {str(e)}")
        
    def get_provider(self, credential_id: UUID):
        try:
            statement = (
                select(Provider)
                .select_from(Credential)
                .join(Provider, Credential.provider_id == Provider.provider_id)
                .where(Credential.credential_id == credential_id)
            )
            provider = self.session.execute(statement).one_or_none()

            if provider is None:
                raise HTTPException(status_code=404, detail="Store not found")

            return provider[0]

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error retrieving store: {str(e)}")        