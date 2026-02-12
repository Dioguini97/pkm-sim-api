from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from dotenv import load_dotenv

load_dotenv()
class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    environment: str = 'develop'
    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ALGORITHM: str = os.getenv('ALGORITHM')

    class Config:
        env_file = '.env.test' if os.getenv('TESTING') else '.env'
        env_file_encoding = 'utf-8'
        extra='ignore'

settings = Settings()