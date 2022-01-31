from app import app
from typing import Literal, List
from app.models import Prediction

values = ["home", "away"]


def get_predictions(match_ids: List[int], user_id: int) -> List[Prediction]:
    return (
        app.session.query(Prediction)
        .filter(Prediction.match_id.in_(match_ids))
        .filter_by(user_id=user_id)
        .all()
    )


def upsert_prediction(
    match_id: int, user_id: int, choice: Literal["home", "away"]
) -> None:
    if choice not in ["home", "away"]:
        return

    prediction = (
        app.session.query(Prediction)
        .filter_by(match_id=match_id)
        .filter_by(user_id=user_id)
        .first()
    )

    if prediction:
        # Update
        prediction.pick = values.index(choice)
    else:
        # Insert
        app.session.add(
            Prediction(match_id=match_id, user_id=user_id, pick=values.index(choice))
        )


def choice_to_string(choice: int):
    return values[choice]
