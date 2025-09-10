from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from fastapi import Depends
from typing import Annotated
import os


BASE_URL = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_URL, "app.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

def create_database_and_tables():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
