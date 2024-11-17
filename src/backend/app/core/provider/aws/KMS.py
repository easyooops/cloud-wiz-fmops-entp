import os
from boto3.session import Session
from botocore.exceptions import ClientError
from dotenv import load_dotenv

class KMSService:
    def __init__(self):
        self.load_credentials()
        self.kms_client = self.create_kms_client()

    def load_credentials(self):
        load_dotenv()
        self.environment = os.getenv("ENVIRONMENT", "local")
        self.aws_region = os.getenv("INNER_AWS_REGION", "us-east-1")

        if self.environment == 'local':
            self.aws_access_key_id = os.getenv("INNER_AWS_ACCESS_KEY_ID")
            self.aws_secret_access_key = os.getenv("INNER_AWS_SECRET_ACCESS_KEY")
        else:
            self.aws_access_key_id = None
            self.aws_secret_access_key = None

    def create_kms_client(self):
        if self.environment == 'local':
            session = Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
        else:
            session = Session(region_name=self.aws_region)

        kms_client = session.client('kms')
        return kms_client

    def encrypt(self, key_id, plaintext):
        try:
            response = self.kms_client.encrypt(
                KeyId=key_id,
                Plaintext=plaintext
            )
            return response['CiphertextBlob']
        except ClientError as e:
            print(e)
            return None

    def decrypt(self, ciphertext_blob):
        try:
            response = self.kms_client.decrypt(
                CiphertextBlob=ciphertext_blob
            )
            return response['Plaintext']
        except ClientError as e:
            print(e)
            return None
