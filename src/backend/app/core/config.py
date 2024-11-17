from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str
    
    # AWS
    COGNITO_REGION: str

    class Config:
        env_file = ".app.env"

settings = Settings()