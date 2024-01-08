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

    #App secret key
    # SECRET_KEY: str = os.environ.get('SECRET_KEY')

def get_settings() -> Settings:
    return Settings()