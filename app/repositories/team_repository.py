from dataclasses import dataclass

from app.database import Session
from app.models import Team


@dataclass
class TeamInfo:
    full_name: str
    abbreviation: str

    def logo(self) -> str:
        return f"{self.abbreviation}.webp"


abbreviations = [
    "ARI",
    "ATL",
    "BAL",
    "BUF",
    "CAR",
    "CHI",
    "CIN",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GB",
    "HOU",
    "IND",
    "JAX",
    "KC",
    "LV",
    "LAC",
    "LA",
    "MIA",
    "MIN",
    "NYJ",
    "NYG",
    "NO",
    "NE",
    "PHI",
    "PIT",
    "SF",
    "SEA",
    "TB",
    "TEN",
    "WAS",
]


class TeamRepository:
    def __init__(self) -> None:
        self.teams = Session.query(Team).all()

    def get_team(self, index: int) -> Team:
        return self.teams[index - 1]

    def get_team_info(self, index: int) -> TeamInfo:
        team = self.teams[index - 1]
        full_name = team.city_name + " " + team.team_name
        abbr = abbreviations[index - 1]

        return TeamInfo(full_name=full_name, abbreviation=abbr)

    def get_team_name(self, index: int) -> str:
        team = self.get_team(index)
        return team.city_name + " " + team.team_name
