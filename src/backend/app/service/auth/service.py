import json
import os
import logging
from dotenv import load_dotenv
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer
from google.auth.transport import requests as google_requests
from jose import jwt, JWTError, ExpiredSignatureError
from datetime import datetime, timedelta
from google.auth.transport import requests
from google.oauth2 import id_token
import requests
from fastapi import Depends, HTTPException, Security
from uuid import UUID
from app.service.credential.model import Credential
from fastapi import HTTPException, Security
from app.core.provider.aws.SecretManager import SecretManagerService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
load_dotenv()

logging.basicConfig(level=logging.INFO)
class AuthService:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    AUTH_SECRET_KEY = os.getenv("AUTH_SECRET_KEY")
    ALGORITHM = "HS256"                                 # 사용할 알고리즘
    ACCESS_TOKEN_EXPIRE_MINUTES = 30                    # 엑세스 토큰 유효 시간 (default 30분)
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_TOKEN_URI = os.getenv("GOOGLE_TOKEN_URI")
    ENV = os.getenv("ENVIRONMENT")

    @staticmethod
    def verify_google_token(token: str):
        try:
            idinfo = id_token.verify_oauth2_token(token, google_requests.Request(), AuthService.GOOGLE_CLIENT_ID)

            if idinfo['aud'] != AuthService.GOOGLE_CLIENT_ID:
                raise ValueError('Invalid client ID.')
            
            user_id = idinfo['sub']
            email = idinfo['email']
            name = idinfo['family_name']

            return {'user_id': user_id, 'email': email, 'name': name}
        except ValueError as e:
            logging.error(f"Invalid token: {e}")
            raise HTTPException(status_code=403, detail="Invalid token")

    @staticmethod
    def exchange_code_for_tokens(code: str):
        logging.info(f'Exchanging code for tokens with code: {code}')

        if AuthService.ENV == 'local':
            redirect_uri = 'http://localhost:11006/google/callback'
        else:
            redirect_uri = 'https://management.cloudwiz-ai.com/google/callback'

        data = {
            'code': code,
            'client_id': AuthService.GOOGLE_CLIENT_ID,
            'client_secret': AuthService.GOOGLE_CLIENT_SECRET,
            'redirect_uri': redirect_uri,
            'grant_type': 'authorization_code'
        }
        response = requests.post(AuthService.GOOGLE_TOKEN_URI, data=data)
        if response.status_code == 200:
            logging.info('Tokens received successfully.')
            return response.json()
        else:
            logging.error(f'Failed to retrieve token: {response.status_code} {response.text}')
            raise HTTPException(status_code=response.status_code, detail="Failed to retrieve token")

    @staticmethod
    def save_tokens_to_db(session: Session, user_id: UUID, provider_id: str, access_token: str, refresh_token: str, expires_in: int):
        credential = Credential(
            user_id=user_id,
            provider_id=provider_id,
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in
        )
        session.add(credential)
        session.commit()

    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=AuthService.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AuthService.AUTH_SECRET_KEY, algorithm=AuthService.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=AuthService.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, AuthService.AUTH_SECRET_KEY, algorithm=AuthService.ALGORITHM)

    @staticmethod
    def verify_jwt_token(token: str):
        try:
            payload = jwt.decode(token, AuthService.AUTH_SECRET_KEY, algorithms=[AuthService.ALGORITHM])
            user_id: str = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    def refresh_access_token(refresh_token: str):
        data = {
            'client_id': AuthService.GOOGLE_CLIENT_ID,
            'client_secret': AuthService.GOOGLE_CLIENT_SECRET,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post(AuthService.GOOGLE_TOKEN_URI, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to refresh access token")

    def get_openai_key():
        # secret_manager = SecretManagerService()
        # secret_name = os.getenv("SECRETS_MANAGER_NAME")
        # secret_value  = secret_manager.get_secret(secret_name)
        # secrets = json.loads(secret_value)
        # return secrets.get("OPENAI_API_KEY")
        return os.getenv("OPENAI_API_KEY")

    def get_aws_key():
        # secret_manager = SecretManagerService()
        # secret_name = os.getenv("SECRETS_MANAGER_NAME")
        # secret_value  = secret_manager.get_secret(secret_name)
        # secrets = json.loads(secret_value)
        # return {
        #     'aws_access_key': secrets.get("AWS_ACCESS_KEY_ID"),
        #     'aws_secret_access_key': secrets.get("AWS_SECRET_ACCESS_KEY"),
        #     'aws_region': secrets.get("AWS_REGION")
        # }
        return {
            'aws_access_key': os.getenv("AWS_ACCESS_KEY_ID"),
            'aws_secret_access_key': os.getenv("AWS_SECRET_ACCESS_KEY"),
            'aws_region': os.getenv("AWS_REGION")
        }

    def get_db_info():
        # secret_manager = SecretManagerService()
        # secret_name = os.getenv("SECRETS_MANAGER_NAME")
        # secret_value  = secret_manager.get_secret(secret_name)
        # secrets = json.loads(secret_value)
        # return secrets.get("DATABASE_URL")
        return os.getenv("DATABASE_URL")

def get_current_user(token: str = Security(oauth2_scheme)):
    return AuthService.verify_jwt_token(token)
