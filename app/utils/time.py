from datetime import datetime
from flask import g
from pytz import timezone, utc

eastern = timezone("US/Eastern")

def get_request_time():
    return g.request_time

def to_eastern(value: datetime, timezone=eastern, format="%Y-%m-%d %H:%M") -> str:
    utc_dt = value.astimezone(utc) if value.tzinfo else utc.localize(value)
    local_dt = utc_dt.astimezone(timezone)

    return f"{local_dt.strftime(format)} {local_dt.tzname()}"