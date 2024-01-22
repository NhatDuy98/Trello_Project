import os
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth
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

    #OAuth2 Google
    CLIENT_ID: str = os.environ.get('CLIENT_ID')
    CLIENT_SECRET: str = os.environ.get('CLIENT_SECRET')
    SESSION_SECRET: str = os.environ.get('SESSION_SECRET')

def get_settings() -> Settings:
    return Settings()

def get_oath():
    settings = get_settings()

    config_data = {
        'GOOGLE_CLIENT_ID': settings.CLIENT_ID,
        'GOOGLE_CLIENT_SECRET': settings.CLIENT_SECRET
    }

    starlette_config = Config(environ = config_data)
    oauth = OAuth(starlette_config)
    oauth.register(
        name = 'google',
        server_metadata_url = 'https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs = {'scope': 'openid email profile'}
    )

    return oauth