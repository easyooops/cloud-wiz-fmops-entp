from typing import Dict, List  
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient  
from app.core.interface.service import ServiceFactory, StorageService  
  
class AzureStorageService(StorageService):  
    def __init__(self, account_name, account_key, container_name, sas_token=None):  
        self.account_name = account_name  
        self.account_key = account_key  
        self.container_name = container_name  
        self.sas_token = sas_token  
        self.client = self.create_azure_client()  
        self.container_client = self.create_container_if_not_exists()  
  
    def create_azure_client(self):  
        if self.sas_token:  
            connection_string = f"BlobEndpoint=https://{self.account_name}.blob.core.windows.net/;SharedAccessSignature={self.sas_token}"  
        else:  
            connection_string = f"DefaultEndpointsProtocol=https;AccountName={self.account_name};AccountKey={self.account_key};EndpointSuffix=core.windows.net"  
        return BlobServiceClient.from_connection_string(connection_string)  
  
    def create_container_if_not_exists(self):  
        container_client = self.client.get_container_client(self.container_name)  
        try:  
            container_client.get_container_properties()  
            print(f"Container {self.container_name} already exists.")  
        except Exception as e:  
            print(f"Container {self.container_name} does not exist, creating it.")  
            container_client.create_container()  
            print(f"Container {self.container_name} created.")  
        return container_client  
  
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
            blob_client = self.container_client.get_blob_client(directory_name + '/')  
            blob_client.upload_blob('', overwrite=True)  
            print(f"Directory {directory_name} created.")  
        return self.retry(create)  
  
    def list_objects(self, directory_name: str = ''):  
        blobs = self.container_client.list_blobs(name_starts_with=directory_name)  
        return [blob.name for blob in blobs]  
  
    def list_all_objects(self, directory_name: str = '') -> List[Dict]:  
        blobs = self.container_client.list_blobs(name_starts_with=directory_name)  
        return [  
            {  
                'Key': blob.name,  
                'LastModified': blob.last_modified,  
                'Size': blob.size  
            }  
            for blob in blobs if not blob.name.endswith('/')  
        ]  
      
    def list_files(self, directory_name: str = '') -> List[Dict]:  
        return self.list_all_objects(directory_name)  
  
    def get_directory_info(self, directory_name: str = ''):  
        blobs = self.container_client.list_blobs(name_starts_with=directory_name)  
        total_size = sum(blob.size for blob in blobs)  
        file_count = len([blob for blob in blobs if not blob.name.endswith('/')])  
        return {'total_size': total_size, 'file_count': file_count}  
  
    def upload_file(self, file, file_location: str):  
        try:  
            blob_client = self.container_client.get_blob_client(file_location)  
            blob_client.upload_blob(file, overwrite=True)  
        except Exception as e:  
            print(f"Error uploading file: {e}")  
  
    def delete_file(self, key: str):  
        try:  
            blob_client = self.container_client.get_blob_client(key)  
            blob_client.delete_blob()  
        except Exception as e:  
            print(f"Error deleting file: {e}")  
  
    def delete_bucket(self):  
        try:  
            self.container_client.delete_container()  
        except Exception as e:  
            print(f"Error deleting container: {e}")  
  
    def delete_directory(self, directory_name: str):  
        blobs = self.container_client.list_blobs(name_starts_with=directory_name)  
        for blob in blobs:  
            blob_client = self.container_client.get_blob_client(blob.name)  
            blob_client.delete_blob()  
  
    def download_file(self, file_key: str, local_file_path: str):  
        try:  
            blob_client = self.container_client.get_blob_client(file_key)  
            with open(local_file_path, "wb") as download_file:  
                download_file.write(blob_client.download_blob().readall())  
        except Exception as e:  
            print(f"Error downloading file: {e}")  
            raise  
  
    def set_ready(self):  
        print("AzureStorageService is ready")  
  
    def teardown(self):  
        print("AzureStorageService is being torn down")  
  
class AzureStorageServiceFactory(ServiceFactory):  
    def __init__(self, account_name, account_key, container_name, sas_token=None):  
        self.account_name = account_name  
        self.account_key = account_key  
        self.container_name = container_name  
        self.sas_token = sas_token  
  
    def create(self) -> AzureStorageService:  
        return AzureStorageService(  
            account_name=self.account_name,  
            account_key=self.account_key,  
            container_name=self.container_name,  
            sas_token=self.sas_token  
        )  