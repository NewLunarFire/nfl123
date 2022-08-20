from app import app
from typing import List
from app.models import Match


def get_match(match_id: int) -> Match:
    return app.session.query(Match).filter_by(id=match_id).first()


def get_matches_for_week(week: int) -> List[Match]:
    return app.session.query(Match).filter_by(week=week).all()


def get_matches_for_weeks(weeks: List[int]) -> List[Match]:
    return app.session.query(Match).filter(Match.week.in_(weeks)).all()


def get_all_matches() -> List[Match]:
    return app.session.query(Match).all()
