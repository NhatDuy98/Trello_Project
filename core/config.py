import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import quote_plus
from pydantic_settings import BaseSettings

env_path = Path(".") / ".env"
load_dotenv(dotenv_path = env_path)

class Settings(BaseSettings):

    #Database MySQL config
    MYSQL_USER: str = os.environ.get('MYSQL_USER')
    MYSQL_PASSWORD: str = os.environ.get('MYSQL_PASSWORD')
    MYSQL_DB: str = os.environ.get('MYSQL_DB')
    MYSQL_SERVER: str = os.environ.get('MYSQL_SERVER')
    MYSQL_PORT: str = os.environ.get('MYSQL_PORT')
    DATABASE_URL: str = f"mysql+pymysql://{MYSQL_USER}:%s@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}" % quote_plus(MYSQL_PASSWORD)

    #JWT
    # import secrets
    # print(secrets.token_hex(32))
    # create secret token   
    JWT_SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.environ.get('JWT_ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

    END_POINT_V1: str = "/api/v1"
    END_POINT_BOARD: str = 'boards'
    END_POINT_MEMBER: str = 'members'

    END_POINT_LABEL: str = 'labels'
    END_POINT_CARD: str = 'cards'
    END_POINT_LABEL_CARD: str = 'card_labels'

def get_settings() -> Settings:
    return Settings()