from typing import Dict, List
from boto3.session import Session
from botocore.exceptions import ClientError
from app.core.interface.service import ServiceFactory, StorageService

class S3StorageService(StorageService):
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region
        self.bucket_name = bucket_name
        self.s3_client = self.create_s3_client()
        self.create_bucket_if_not_exists()

    def create_s3_client(self):
        session = Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.aws_region
        )
        s3_client = session.client('s3')
        return s3_client

    def create_bucket_if_not_exists(self):
        try:
            # 버킷이 존재하는지 확인합니다.
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket {self.bucket_name} already exists.")
        except ClientError as e:

            error_code = e.response['Error']['Code']
            if error_code == '404':
                # 버킷이 존재하지 않는 경우 생성합니다.
                try:
                    self.create_bucket()
                    print("Bucket created, waiting for stabilization...")
                    import time
                    time.sleep(10)
                except ClientError as e:
                    print(f"Error while creating bucket: {e}")
                    raise
            elif error_code == '403':
                print("Access to the bucket is forbidden. Check your AWS credentials and permissions.")
                raise
            else:
                print(f"Error while checking if bucket exists: {e}")
                raise

    def create_bucket(self):
        try:
            if self.aws_region == 'us-east-1':
                response = self.s3_client.create_bucket(Bucket=self.bucket_name)
            else:
                response = self.s3_client.create_bucket(
                    Bucket=self.bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': self.aws_region}
                )
            print(f"Bucket creation response: {response}")
            return response
        except ClientError as e:
            print(f"Error while creating bucket: {e}")
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

    def create_directory(self, directory_name: str):
        def create():
            response = self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=directory_name + '/'
            )
            print(f"Directory creation response: {response}")
            return response

        return self.retry(create)

    def list_objects(self, directory_name: str = ''):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=directory_name)
            return response.get('Contents', [])
        except ClientError as e:
            print(e)
            return []

    def list_all_objects(self, directory_name: str = '') -> List[Dict]:
        if directory_name and not directory_name.endswith('/'):
            directory_name += '/'

        try:
            all_objects = []
            continuation_token = None

            while True:
                if continuation_token:
                    response = self.s3_client.list_objects_v2(
                        Bucket=self.bucket_name,
                        Prefix=directory_name,
                        ContinuationToken=continuation_token
                    )
                else:
                    response = self.s3_client.list_objects_v2(
                        Bucket=self.bucket_name,
                        Prefix=directory_name
                    )

                contents = response.get('Contents', [])
                all_objects.extend(contents)

                if response.get('IsTruncated'):
                    continuation_token = response.get('NextContinuationToken')
                else:
                    break

            filtered_objects = [obj for obj in all_objects if not obj['Key'].endswith('/')]

            if not filtered_objects:
                print(f"No objects found in directory: {directory_name}")
                return []

            return filtered_objects
        except ClientError as e:
            print(f"An error occurred: {e}")
            return []

    def list_files(self, directory_name: str = '') -> List[Dict]:
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=directory_name)
            return response.get('Contents', [])
        except ClientError as e:
            print(e)
            return []
        
    def get_directory_info(self, directory_name: str = ''):
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=directory_name)
            contents = response.get('Contents', [])
            total_size = sum(obj['Size'] for obj in contents)
            file_count = len(contents)-1
            return {
                'total_size': total_size,
                'file_count': file_count
            }
        except ClientError as e:
            print(e)
            return {
                'total_size': 0,
                'file_count': 0
            }
        
    def upload_file(self, file, file_location: str):
        try:
            self.s3_client.upload_fileobj(file, self.bucket_name, file_location)
        except ClientError as e:
            print(e)
                    
    def delete_file(self, key: str):
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            print(e)

    def delete_bucket(self):
        objects = self.list_objects()
        for obj in objects:
            key = obj['Key']
            self.delete_file(key)
        try:
            response = self.s3_client.delete_bucket(Bucket=self.bucket_name)
            return response
        except ClientError as e:
            print(e)
            return None
        
    def delete_directory(self, store_name: str):
        try:
            objects_to_delete = self.list_objects(store_name)
            delete_keys = [{'Key': obj['Key']} for obj in objects_to_delete]

            if delete_keys:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': delete_keys}
                )
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=f"{store_name}/")
        except ClientError as e:
            print(e)     
            
    def download_file(self, s3_file_key: str, local_file_path: str):
        try:
            self.s3_client.download_file(self.bucket_name, s3_file_key, local_file_path)
        except ClientError as e:
            print(f"Error downloading file from S3: {str(e)}")
            raise

    def set_ready(self):
        print("S3StorageService is ready")

    def teardown(self):
        print("S3StorageService is being torn down")


class S3StorageServiceFactory(ServiceFactory):
    def __init__(self, aws_access_key_id, aws_secret_access_key, aws_region, bucket_name):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.aws_region = aws_region
        self.bucket_name = bucket_name

    def create(self) -> S3StorageService:
        return S3StorageService(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            aws_region=self.aws_region,
            bucket_name=self.bucket_name
        )