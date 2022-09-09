from typing import List

from sqlalchemy import or_

from app.database import Session
from app.models import Match


def get_match(match_id: int) -> Match:
    return __query_match().filter_by(id=match_id).first()


def get_matches_for_week(week: int) -> List[Match]:
    return __query_match().filter_by(week=week).all()


def get_matches_for_weeks(weeks: List[int]) -> List[Match]:
    return __query_match().filter(Match.week.in_(weeks)).all()


def get_matches_for_team(team_id: int) -> List[Match]:
    return (
        __query_match()
        .filter(or_(Match.away_team == team_id, Match.home_team == team_id))
        .all()
    )


def get_all_matches() -> List[Match]:
    return __query_match().all()


def __query_match():
    return Session.query(Match).order_by(Match.start_time).order_by(Match.id)
