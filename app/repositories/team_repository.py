from app import app
from app.models import Team

logos = [
    "ARI.webp",
    "ATL.webp",
    "BAL.webp",
    "BUF.webp",
    "CAR.webp",
    "CHI.webp",
    "CIN.webp",
    "CLE.webp",
    "DAL.webp",
    "DEN.webp",
    "DET.webp",
    "GB.webp",
    "HOU.webp",
    "IND.webp",
    "JAX.webp",
    "KC.webp",
    "LV.webp",
    "LAC.webp",
    "LA.webp",
    "MIA.webp",
    "MIN.webp",
    "NYJ.webp",
    "NYG.webp",
    "NO.webp",
    "NE.webp",
    "PHI.webp",
    "PIT.webp",
    "SF.webp",
    "SEA.webp",
    "TB.webp",
    "TEN.webp",
    "WAS.webp",
]


class TeamRepository:
    def __init__(self) -> None:
        self.teams = app.session.query(Team).all()

    def get_team(self, index: int) -> Team:
        return self.teams[index - 1]

    def get_team_name(self, index: int) -> str:
        team = self.get_team(index)
        return team.city_name + " " + team.team_name

    @staticmethod
    def get_team_logo(index: int) -> str:
        return logos[index - 1]
