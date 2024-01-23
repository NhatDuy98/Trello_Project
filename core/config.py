import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path = env_path)

class Settings(BaseSettings):

    #Database MySQL config
    MYSQL_USER: str = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD: str = os.environ.get('MYSQL_PASSWORD', '123456')
    MYSQL_DB: str = os.environ.get('MYSQL_DB', 'trello')
    MYSQL_SERVER: str = os.environ.get('MYSQL_SERVER', 'localhost')
    MYSQL_PORT: str = os.environ.get('MYSQL_PORT', 3306)
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:%s@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}" % quote_plus(MYSQL_PASSWORD)

    #JWT
    # import secrets
    # print(secrets.token_hex(32))
    # create secret token   
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY", "08c8b8a7405d3db1e0738228f6d9e2499eb8114fd83f01bf9de4f35ae952d720")
    JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30)

    END_POINT_V1: str = '/api/v1'
    END_POINT_LABEL: str = 'labels'
    END_POINT_CARD: str = 'cards'
    END_POINT_LABEL_CARD: str = 'card_labels'

def get_settings() -> Settings:
    return Settings()