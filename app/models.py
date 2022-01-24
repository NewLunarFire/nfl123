from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Date
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
