from app import app
from app.models import Match, User
from datetime import datetime
from flask import request
from app.authentication import authenticated
from app.repositories.match import get_matches_for_week
from app.repositories.results import is_ot
from app.repositories.team_repository import TeamRepository

from app.repositories.predictions import (
    get_predictions,
    upsert_prediction,
    choice_to_string,
    is_game_started
)
from app.utils import get_request_time, render
from flask import redirect

teams = TeamRepository()

def get_current_week():
    return 1

@app.route("/week")
@authenticated()
def default_week(user: User):
    current_week = get_current_week()
    return redirect(f"week/{current_week}")

@app.route("/week/<week>", methods=["GET", "POST"])
@authenticated()
def week(user: User, week: int):
    request_time = get_request_time()
    if request.method == "POST" and user:
        process_picks(request.form, user.id, request_time)

    matches = get_matches_for_week(week=week)

    predictions = (
        {
            prediction.match_id: choice_to_string(prediction.pick)
            for prediction in get_predictions(
                match_ids=[match.id for match in matches], user_id=user.id
            )
        }
        if user
        else {}
    )

    matches = [to_dict(match, predictions.get(match.id), request_time) for match in matches]
    points = sum([match.get("user_score", 0) for match in matches])
    score = sum([match.get("user_win", False) for match in matches])
    total_matches = sum([match["final"] for match in matches])

    return render(
        "week.html",
        week=week,
        matches=matches,
        predictions=predictions,
        points=points,
        score=score,
        total_matches=total_matches,
        points_color=points_color,
        score_color=score_color,
    )


def to_dict(match: Match, pick: str, request_time: datetime) -> dict:
    result = {}
    prediction = {}

    if match.result:
        result = {
            "home_score": match.result.home_score,
            "away_score": match.result.away_score,
            "ot": is_ot(match.result.result_type),
        }

        if pick:
            if pick == "home":
                score = match.result.home_score - match.result.away_score
                win = match.result.home_score >= match.result.away_score
            else:
                score = match.result.away_score - match.result.home_score
                win = match.result.away_score >= match.result.home_score
        else:
            score = -abs(match.result.home_score - match.result.away_score)
            win = False

        prediction = {"user_score": score, "user_win": win}

    return {
        **result,
        **prediction,
        "home_team": teams.get_team_name(match.home_team),
        "away_team": teams.get_team_name(match.away_team),
        "start_time": match.start_time,
        "id": match.id,
        "final": bool(match.result),
        "locked": is_game_started(request_time=request_time, match=match)
    }


def process_picks(picks: dict, user_id: int, request_time: datetime) -> None:
    for key, value in picks.items():
        if key.startswith("match_"):
            match_id = int(key[6:])
            upsert_prediction(match_id=match_id, user_id=user_id, choice=value, request_time=request_time)

    app.session.commit()


def points_color(points: int) -> str:
    return "green" if points >= 0 else "red"


def score_color(score: int, total: int) -> str:
    if total == 0:
        return "unset"

    pct = score / total
    if pct > 0.6:
        return "green"
    elif pct > 0.4:
        return "orange"
    else:
        return "red"
