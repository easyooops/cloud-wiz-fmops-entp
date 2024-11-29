import boto3  
from botocore.exceptions import NoCredentialsError, PartialCredentialsError  
from app.components.DocumentLoader.Base import BaseDocumentLoader

class S3DocumentLoader(BaseDocumentLoader):  
    def __init__(self, bucket_name, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None, region_name=None):  
        super().__init__()  
        self.bucket_name = bucket_name  
        self.s3_client = boto3.client(  
            's3',  
            aws_access_key_id=aws_access_key_id,  
            aws_secret_access_key=aws_secret_access_key,  
            aws_session_token=aws_session_token,  
            region_name=region_name  
        )  
  
    def load(self):  
        try:  
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name)  
            if 'Contents' not in response:  
                raise ValueError("No objects found in the bucket.")  
  
            self.documents = []  
            for obj in response['Contents']:  
                obj_key = obj['Key']  
                obj_response = self.s3_client.get_object(Bucket=self.bucket_name, Key=obj_key)  
                content = obj_response['Body'].read()  
                self.documents.append(content)  
  
        except NoCredentialsError:  
            raise ValueError("AWS credentials not provided.")  
        except PartialCredentialsError:  
            raise ValueError("Incomplete AWS credentials provided.")  
        except Exception as e:  
            raise ValueError(f"An error occurred: {str(e)}")  
  
    def process_documents(self):  
        if self.documents is None:  
            raise ValueError("Documents are not loaded yet. Call the load method first.")  
        # 예시로, 문서의 내용을 텍스트로 변환하여 저장하는 과정  
        processed_documents = []  
        for doc in self.documents:  
            processed_documents.append(doc.decode("utf-8"))  
        self.documents = processed_documents  