from app import app
from app.models import Team


class TeamRepository:
    def __init__(self) -> None:
        self.teams = app.session.query(Team).all()

    def get_team(self, index: int) -> Team:
        return self.teams[index - 1]

    def get_team_name(self, index: int) -> str:
        team = self.get_team(index)
        return team.city_name + " " + team.team_name
