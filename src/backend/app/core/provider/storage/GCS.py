from typing import Dict, List
from google.cloud import storage  
from google.auth.exceptions import DefaultCredentialsError  
from app.core.interface.service import ServiceFactory, StorageService  
  
class GCSStorageService(StorageService):  
    def __init__(self, project_id, bucket_name, credentials_json):  
        self.project_id = project_id  
        self.bucket_name = bucket_name  
        self.credentials_json = credentials_json  
        self.client = self.create_gcs_client()  
        self.bucket = self.create_bucket_if_not_exists()  
  
    def create_gcs_client(self):  
        try:  
            client = storage.Client.from_service_account_json(self.credentials_json)  
            return client  
        except DefaultCredentialsError as e:  
            print(f"Error while creating GCS client: {e}")  
            raise  
  
    def create_bucket_if_not_exists(self):  
        try:  
            bucket = self.client.get_bucket(self.bucket_name)  
            print(f"Bucket {self.bucket_name} already exists.")  
        except Exception as e:  
            print(f"Bucket {self.bucket_name} does not exist, creating it.")  
            bucket = self.client.create_bucket(self.bucket_name)  
            print(f"Bucket {self.bucket_name} created.")  
        return bucket  
  
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
  
    def create_directory(self, directory_name: str):  
        def create():  
            blob = self.bucket.blob(directory_name + '/')  
            blob.upload_from_string('')  
            print(f"Directory {directory_name} created.")  
        return self.retry(create)  
  
    def list_objects(self, directory_name: str = ''):  
        blobs = self.client.list_blobs(self.bucket_name, prefix=directory_name)  
        return [blob.name for blob in blobs]  
  
    def list_all_objects(self, directory_name: str = '') -> List[Dict]:  
        blobs = self.client.list_blobs(self.bucket_name, prefix=directory_name)  
        return [{'Key': blob.name, 'Size': blob.size} for blob in blobs if not blob.name.endswith('/')]  
  
    def list_files(self, directory_name: str = '') -> List[Dict]:  
        return self.list_all_objects(directory_name)  
  
    def get_directory_info(self, directory_name: str = ''):  
        blobs = self.client.list_blobs(self.bucket_name, prefix=directory_name)  
        total_size = sum(blob.size for blob in blobs)  
        file_count = len([blob for blob in blobs if not blob.name.endswith('/')])  
        return {'total_size': total_size, 'file_count': file_count}  
  
    def upload_file(self, file, file_location: str):  
        try:  
            blob = self.bucket.blob(file_location)  
            blob.upload_from_file(file)  
        except Exception as e:  
            print(f"Error uploading file: {e}")  
  
    def delete_file(self, key: str):  
        try:  
            blob = self.bucket.blob(key)  
            blob.delete()  
        except Exception as e:  
            print(f"Error deleting file: {e}")  
  
    def delete_bucket(self):  
        try:  
            self.bucket.delete(force=True)  
        except Exception as e:  
            print(f"Error deleting bucket: {e}")  
  
    def delete_directory(self, directory_name: str):  
        blobs = self.bucket.list_blobs(prefix=directory_name)  
        for blob in blobs:  
            blob.delete()  
  
    def download_file(self, file_key: str, local_file_path: str):  
        try:  
            blob = self.bucket.blob(file_key)  
            blob.download_to_filename(local_file_path)  
        except Exception as e:  
            print(f"Error downloading file: {e}")  
            raise  
  
    def set_ready(self):  
        print("GCSStorageService is ready")  
  
    def teardown(self):  
        print("GCSStorageService is being torn down")  
  
class GCSStorageServiceFactory(ServiceFactory):  
    def __init__(self, project_id, bucket_name, credentials_json):  
        self.project_id = project_id  
        self.bucket_name = bucket_name  
        self.credentials_json = credentials_json  
  
    def create(self) -> GCSStorageService:  
        return GCSStorageService(  
            project_id=self.project_id,  
            bucket_name=self.bucket_name,  
            credentials_json=self.credentials_json  
        )  