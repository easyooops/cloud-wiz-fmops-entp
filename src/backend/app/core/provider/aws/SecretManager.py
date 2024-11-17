import os
from boto3.session import Session
from botocore.exceptions import ClientError
from dotenv import load_dotenv

class SecretManagerService:
    def __init__(self):
        self.load_credentials()
        self.secrets_client = self.create_secrets_client()

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

    def create_secrets_client(self):
        if self.environment == 'local':
            session = Session(
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.aws_region
            )
        else:
            session = Session(region_name=self.aws_region)

        secrets_client = session.client('secretsmanager')
        return secrets_client

    def get_secret(self, secret_name):
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in response:
                return response['SecretString']
            else:
                return response['SecretBinary']
        except ClientError as e:
            print(e)
            return None

    def create_secret(self, name, secret_string):
        try:
            response = self.secrets_client.create_secret(
                Name=name,
                SecretString=secret_string
            )
            return response
        except ClientError as e:
            print(e)
            return None

    def update_secret(self, secret_id, secret_string):
        try:
            response = self.secrets_client.update_secret(
                SecretId=secret_id,
                SecretString=secret_string
            )
            return response
        except ClientError as e:
            print(e)
            return None

    def delete_secret(self, secret_id, recovery_window_in_days=30):
        try:
            response = self.secrets_client.delete_secret(
                SecretId=secret_id,
                RecoveryWindowInDays=recovery_window_in_days
            )
            return response
        except ClientError as e:
            print(e)
            return None
