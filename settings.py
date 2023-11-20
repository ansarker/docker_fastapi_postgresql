from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    API_v1_STR: str = "/api/v1"
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    PROJECT_NAME: str = "Book Service"
    PROJECT_DESC: str = "A simple book service application."
    DB_URL: str = os.environ.get("DB_URL")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        os.environ.get("ORIGIN_1"),
        os.environ.get("ORIGIN_2"),
    ]

    class Config:
        case_sensitive = True

settings = Settings()