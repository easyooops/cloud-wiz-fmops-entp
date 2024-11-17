import base64
import requests
from app.core.interface.service import ServiceFactory, StorageService

class GitHubStorageService(StorageService):
    def __init__(self, token: str, repo: str, owner: str):
        self.token = token
        self.repo = repo
        self.owner = owner
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}"

    def _headers(self):
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def upload_file(self, file, file_location: str):
        # Read the file and encode it to base64
        content = file.read()
        content_b64 = base64.b64encode(content).decode('utf-8')
        url = f"{self.api_url}/contents/{file_location}"
        
        data = {
            "message": f"Add {file_location}",
            "content": content_b64
        }

        response = requests.put(url, json=data, headers=self._headers())
        if response.status_code == 201:
            print(f"File uploaded: {file_location}")
        else:
            print(f"Failed to upload file: {response.json()}")

    def delete_file(self, key: str):
        # Get the file SHA to delete it
        url = f"{self.api_url}/contents/{key}"
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            sha = response.json()['sha']
            delete_data = {
                "message": f"Delete {key}",
                "sha": sha
            }
            delete_response = requests.delete(url, json=delete_data, headers=self._headers())
            if delete_response.status_code == 200:
                print(f"File deleted: {key}")
            else:
                print(f"Failed to delete file: {delete_response.json()}")
        else:
            print(f"Failed to get file SHA: {response.json()}")

    def list_files(self, directory_name: str = ''):
        url = f"{self.api_url}/contents/{directory_name}"
        response = requests.get(url, headers=self._headers())
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to list files: {response.json()}")
            return []

    def create_directory(self, directory_name: str):
        # GitHub doesn't support empty directories, so we create a placeholder file
        file_location = f"{directory_name}/.gitkeep"
        self.upload_file(file=open('/dev/null', 'rb'), file_location=file_location)

    def set_ready(self):
        print("GitHubStorageService is ready")

    def teardown(self):
        print("GitHubStorageService is being torn down")

class GitHubStorageServiceFactory(ServiceFactory):
    def __init__(self, token: str, repo: str, owner: str):
        self.token = token
        self.repo = repo
        self.owner = owner

    def create(self) -> GitHubStorageService:
        return GitHubStorageService(self.token, self.repo, self.owner)
