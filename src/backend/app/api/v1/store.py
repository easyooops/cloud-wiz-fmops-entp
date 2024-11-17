from typing import Any, Dict, List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session
from app.core.factories import get_database
from app.service.store.service import StoreService
from app.api.v1.schemas.store import StoreCreate, StoreUpdate, StoreWithDirectory, Vector
from app.core.exception import internal_server_error
from app.service.store.model import Store
from app.service.auth.service import get_current_user

router = APIRouter()

@router.get("/{user_id}", response_model=List[StoreWithDirectory])
def get_stores(
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        stores = service.get_all_stores(user_id, None)
    
        store_responses = []
        for store in stores:
            directory_info = service.get_store_directory_info(user_id, store.store_name, store.credential_id)
            store_with_directory = StoreWithDirectory(
                store_id=store.store_id,
                credential_id=store.credential_id,
                store_name=store.store_name,
                description=store.description,
                created_at=store.created_at,
                updated_at=store.updated_at,
                user_id=store.user_id,
                provider_logo=service.get_provider(store.credential_id).logo,
                provider_company=service.get_provider(store.credential_id).company,              
                total_size=directory_info['total_size'],
                file_count=directory_info['file_count']
            )
            store_responses.append(store_with_directory)
        return store_responses
        
    except Exception as e:
        raise internal_server_error(e)

@router.post("/{user_id}", response_model=Store)
def create_store(
    store: StoreCreate,
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        return service.create_store(store, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating store: {str(e)}")

@router.put("/{user_id}/{store_id}", response_model=Store)
def update_store(
    store_id: UUID,
    store_update: StoreUpdate,
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        return service.update_store(store_id, store_update, user_id)
    except Exception as e:
        raise internal_server_error(e)

@router.delete("/{user_id}/{store_id}")
def delete_store(
    store_id: UUID,
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        service.delete_store(store_id, user_id)
        return {"message": "Store deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)

@router.get("/{user_id}/{store_id}/files", response_model=List[Dict[str, Any]])
def get_store_files(
    store_id: UUID,
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        return service.list_files(user_id, store_id)
    except Exception as e:
        raise internal_server_error(e)

@router.post("/{user_id}/{store_id}/upload")
def upload_file_to_store(
    store_id: UUID,
    user_id: UUID,
    file: UploadFile = File(...),
    session: Session = Depends(get_database)
    # token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        service.upload_file_to_store(user_id, store_id, file)
        return {"message": "File uploaded successfully"}
    except Exception as e:
        raise internal_server_error(e)
    
@router.delete("/{user_id}/{store_id}/files/{file_name}")
def delete_file_from_store(
    store_id: UUID,
    file_name: str,
    user_id: UUID,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        service.delete_file_from_store(user_id, store_id, file_name)
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)

@router.put("/{user_id}/{store_id}/indexing")
def create_indexing(
    agent: Vector,
    session: Session = Depends(get_database),
    token: str = Depends(get_current_user) 
):
    try:
        service = StoreService(session)
        service.create_indexing(agent)
        return {"message": "Store deleted successfully"}
    except Exception as e:
        raise internal_server_error(e)