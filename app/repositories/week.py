from datetime import datetime
from typing import List

from app.database import Session
from app.models import Week, WeekType


def get_all_weeks_in_year(year: int) -> List[Week]:
    return Session.query(Week).filter_by(year=year).order_by(Week.start_time).all()


def get_weeks_in_year_by_type(year: int, week_type: WeekType) -> List[Week]:
    return (
        Session.query(Week)
        .filter_by(year=year, type=week_type)
        .order_by(Week.start_time)
        .all()
    )


def get_week(name: str, year: int) -> Week:
    return Session.query(Week).filter_by(year=year, display_name=name).first()


def get_current_week(request_time: datetime):
    return (
        Session.query(Week)
        .filter(Week.start_time <= request_time)
        .order_by(Week.start_time.desc())
        .first()
    )
