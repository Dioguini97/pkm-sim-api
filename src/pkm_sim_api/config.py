from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    mongodb_url: str
    database_name: str
    environment: str = 'develop'

    class Config:
        env_file = '.env.test' if os.getenv('TESTING') else '.env'
        env_file_encoding = 'utf-8'
        extra='ignore'

settings = Settings()