from datetime import datetime, timedelta
from typing import List, Literal

from pytz import utc

from app.database import Session
from app.models import Match, Prediction
from app.repositories.match import get_match

values = ["home", "away"]


def get_predictions(match_ids: List[int], user_id: int) -> List[Prediction]:
    return (
        Session.query(Prediction)
        .filter(Prediction.match_id.in_(match_ids))
        .filter_by(user_id=user_id)
        .all()
    )


def upsert_prediction(
    match_id: int, user_id: int, choice: Literal["home", "away"], request_time: datetime
) -> bool:
    if choice not in ["home", "away"]:
        return False

    if is_game_started(request_time=request_time, match=get_match(match_id=match_id)):
        return False

    prediction = (
        Session.query(Prediction)
        .filter_by(match_id=match_id)
        .filter_by(user_id=user_id)
        .first()
    )

    if prediction:
        # Update
        prediction.pick = values.index(choice)
    else:
        # Insert
        Session.add(
            Prediction(match_id=match_id, user_id=user_id, pick=values.index(choice))
        )
    
    return True


def get_predictions_for_match(match_id: int) -> List[Prediction]:
    return Session.query(Prediction).filter_by(match_id=match_id).all()


def choice_to_string(choice: int) -> str:
    return values[choice]


def is_game_started(request_time: datetime, match: Match) -> bool:
    # 15 minutes from match_start
    buffer = timedelta(minutes=15)

    # For testing purposes
    # request_time = datetime.fromisoformat('2021-09-12T16:35:00')

    return (request_time - utc.localize(match.start_time)) > buffer
