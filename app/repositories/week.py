from datetime import datetime
from app import app
from app.models import Week, WeekType
from datetime import datetime
from typing import List


def get_all_weeks_in_year(year: int) -> List[Week]:
    return app.session.query(Week).filter_by(year=year).order_by(Week.start_time).all()


def get_weeks_in_year_by_type(year: int, type: WeekType) -> List[Week]:
    return (
        app.session.query(Week)
        .filter_by(year=year, type=type)
        .order_by(Week.start_time)
        .all()
    )


def get_week(name: str, year: int) -> Week:
    return app.session.query(Week).filter_by(year=year, display_name=name).first()


def get_current_week(request_time: datetime):
    return (
        app.session.query(Week)
        .filter(Week.start_time <= request_time)
        .order_by(Week.start_time)
        .first()
    )
