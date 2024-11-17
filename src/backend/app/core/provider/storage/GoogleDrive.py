import logging
import os
import tempfile
from fastapi import UploadFile
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from app.core.interface.service import ServiceFactory, StorageService
from typing import List, Dict, Any, Optional


class GoogleDriveStorageService(StorageService):
    def __init__(self, access_token: str = None, refresh_token: str = None):
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        token_uri = os.getenv("GOOGLE_TOKEN_URI")

        if refresh_token:
            self.credentials = Credentials(
                token=None,
                refresh_token=refresh_token,
                token_uri=token_uri,
                client_id=client_id,
                client_secret=client_secret
            )
        elif access_token:
            self.credentials = Credentials(token=access_token)
        else:
            raise ValueError("Either access_token or refresh_token must be provided")

        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    def create_directory(self, directory_name: str):
        file_metadata = {
            'name': directory_name.split('/')[-1],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        parent_folder_id = self.get_parent_folder_id(directory_name)
        if parent_folder_id:
            file_metadata['parents'] = [parent_folder_id]

        file = self.drive_service.files().create(body=file_metadata, fields='id, name').execute()
        logging.debug(f"Directory creation response: {file}")
        return file

    def get_parent_folder_id(self, directory_name: str) -> Optional[str]:
        folders = directory_name.split('/')
        if len(folders) > 1:
            parent_folder_name = '/'.join(folders[:-1])
            try:
                return self.get_folder_id_by_name(parent_folder_name)
            except FileNotFoundError:
                parent_folder = self.create_directory(parent_folder_name)
                return parent_folder['id']
        return None

    def get_folder_hierarchy_id(self, full_directory_name: str) -> str:
        parts = full_directory_name.split('/')
        parent_id = None
        for part in parts:
            try:
                parent_id = self.get_folder_id_by_name(part, parent_id)
            except FileNotFoundError:
                parent_id = self.create_directory(part, parent_id)['id']
        return parent_id

    def delete_directory(self, directory_id: str):
        try:
            query = f"'{directory_id}' in parents and trashed=false"
            results = self.drive_service.files().list(q=query, fields="files(id)").execute()
            items = results.get('files', [])

            for item in items:
                self.drive_service.files().delete(fileId=item['id']).execute()

            self.drive_service.files().delete(fileId=directory_id).execute()
            logging.debug(f"Deleted directory: {directory_id}")
        except Exception as e:
            logging.error(f"Error deleting directory: {str(e)}")
            raise

    def list_files(self, directory_name: str = ''):
        if directory_name:
            folder_id = self.get_folder_id_by_name(directory_name)
            return self.list_files_in_folder(folder_id)
        else:
            return self.list_all_objects()

    def list_all_objects(self, directory_name: str = '') -> List[Dict[str, Any]]:
        try:
            if directory_name:
                folder_id = self.get_folder_id_by_name(directory_name)
                query = f"'{folder_id}' in parents and trashed=false"
            else:
                query = "trashed=false"

            results = self.drive_service.files().list(q=query, pageSize=1000, fields="files(id, name, size)").execute()
            items = results.get('files', [])
            return items
        except Exception as e:
            logging.error(f"Error listing files: {str(e)}")
            return []

    def get_directory_info(self, directory_name: str = ''):
        try:
            folder_id = self.get_folder_hierarchy_id(directory_name)

            response = self.drive_service.files().list(q=f"'{folder_id}' in parents and trashed=false", fields="files(id, name, size)").execute()
            contents = response.get('files', [])

            total_size = sum(int(obj.get('size', 0)) for obj in contents)
            file_count = len(contents)

            return {
                'total_size': total_size,
                'file_count': file_count
            }
        except Exception as e:
            logging.error(f"Error getting directory info: {str(e)}")
            return {
                'total_size': 0,
                'file_count': 0
            }

    def get_file_id_by_name(self, folder_id: str, file_name: str) -> str:
        try:
            response = self.drive_service.files().list(
                q=f"'{folder_id}' in parents and name='{file_name}' and trashed=false",
                fields="files(id, name)"
            ).execute()
            files = response.get('files', [])
            if not files:
                raise FileNotFoundError(f"No file found with the name: {file_name}")
            return files[0]['id']
        except Exception as e:
            logging.error(f"Error finding file by name: {str(e)}")
            raise

    def get_folder_id_by_name(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        try:
            if parent_id:
                query = f"'{parent_id}' in parents and name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            else:
                query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"

            response = self.drive_service.files().list(q=query, fields="files(id, name)").execute()
            folders = response.get('files', [])
            if not folders:
                raise FileNotFoundError(f"No folder found with the name: {folder_name}")
            return folders[0]['id']
        except Exception as e:
            logging.error(f"Error finding folder by name: {str(e)}")
            raise


    def list_files_in_folder(self, folder_id: str) -> List[Dict[str, Any]]:
        try:
            response = self.drive_service.files().list(
                q=f"'{folder_id}' in parents and trashed=false",
                fields="files(id, name, size)"
            ).execute()
            files = response.get('files', [])
            return files
        except Exception as e:
            logging.error(f"Error listing files in folder: {str(e)}")
            raise

    def upload_file_to_folder(self, folder_id: str, file: UploadFile):
        try:
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file.file.read())
                tmp.flush()
                tmp_path = tmp.name

            file_metadata = {'name': file.filename, 'parents': [folder_id]}
            media = MediaFileUpload(tmp_path, resumable=True)
            uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return uploaded_file
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def upload_file(self, file_path: str, file_location: str):
        try:
            folder_id, filename = os.path.split(file_location)
            file_metadata = {'name': filename, 'parents': [folder_id]}
            media = MediaFileUpload(file_path, resumable=True)
            uploaded_file = self.drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            return uploaded_file
        except Exception as e:
            logging.error(f"Error uploading file: {str(e)}")
            raise

    def delete_file(self, file_id: str):
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
        except Exception as e:
            logging.error(f"Error deleting file: {str(e)}")
            raise

    def retry(self, func, retries=5, delay=5, backoff=2):
        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt < retries - 1:
                    import time
                    time.sleep(delay)
                    delay *= backoff
                else:
                    raise e

    def download_file(self, s3_file_key: str, local_file_path: str):
        try:
            request = self.drive_service.files().get_media(fileId=s3_file_key)
            with open(local_file_path, 'wb') as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    print(f"Download {int(status.progress() * 100)}%.")
        except Exception as e:
            print(f"Error downloading file from Google Drive: {str(e)}")
            raise

    def set_ready(self):
        print("GoogleDriveStorageService is ready")

    def teardown(self):
        print("GoogleDriveStorageService is being torn down")

class GoogleDriveStorageServiceFactory(ServiceFactory):
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    def create(self) -> GoogleDriveStorageService:
        return GoogleDriveStorageService(self.access_token, self.refresh_token)