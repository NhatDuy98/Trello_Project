from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from core.config import get_settings
from typing import Generator


settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping = True,
    pool_recycle = 300,
    pool_size = 10,
    max_overflow = 0,
    echo = True,
    echo_pool = "debug"
)

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()