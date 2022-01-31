from sqlalchemy import Column, Integer, String
from sqlalchemy.types import DateTime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)


class Match(Base):
    __tablename__ = "matches"

    id = Column("id", Integer, primary_key=True)
    week = Column("week", String, nullable=False)
    home_team = Column("home_team", Integer, nullable=False)
    away_team = Column("away_team", Integer, nullable=False)
    start_time = Column("start_time", DateTime, nullable=False)


class Team(Base):
    __tablename__ = "teams"

    id = Column("id", Integer, primary_key=True)
    city_name = Column("city_name", String, nullable=False)
    team_name = Column("team_name", String, nullable=False)


class Prediction(Base):
    __tablename__ = "predictions"

    match_id = Column("match_id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, primary_key=True)
    pick = Column("pick", Integer)

    def __repr__(self):
        return (
            "Prediction[match_id="
            + str(self.match_id)
            + " user_id="
            + str(self.user_id)
            + " pick="
            + str(self.pick)
        )
