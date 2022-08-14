from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from os import environ

from sqlalchemy.sql.schema import ForeignKey

database: str =environ["DATABASE_URL"]
if database.startswith("postgres://"):
    database = database.replace("postgres://", "postgresql://")

engine = create_engine(
    database, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
