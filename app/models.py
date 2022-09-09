from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime

from app.enums.week_type import WeekType

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", String, nullable=False)
    is_admin = Column("is_admin", Boolean, nullable=False)
    lang = Column("lang", String, nullable=False)
    password = Column("password", String, nullable=False)


class Match(Base):
    __tablename__ = "matches"

    id = Column("id", Integer, primary_key=True)
    week = Column("week", String, nullable=False)
    home_team = Column("home_team", Integer, nullable=False)
    away_team = Column("away_team", Integer, nullable=False)
    start_time = Column("start_time", DateTime, nullable=False)

    week_rel = relationship(
        "Week", uselist=False, foreign_keys=[week], primaryjoin="Week.id == Match.week"
    )
    result = relationship("MatchResult", uselist=False, back_populates="match")


class MatchResult(Base):
    __tablename__ = "match_results"

    match_id = Column("match_id", Integer, ForeignKey("matches.id"), primary_key=True)
    result_type = Column("result_type", Integer, nullable=False)
    home_score = Column("home_score", Integer, nullable=False)
    away_score = Column("away_score", Integer, nullable=False)

    match = relationship("Match", uselist=False, back_populates="result")


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


class Week(Base):
    __tablename__ = "weeks"

    id = Column("id", Integer, primary_key=True)
    display_name = Column("display_name", String, nullable=False)
    year = Column("year", Integer, nullable=False)
    type = Column("type", Enum(WeekType), nullable=False)
    start_time = Column("start_time", DateTime, nullable=False)
