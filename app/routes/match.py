from app import app
from app.models import Match, Prediction
from flask import session, request
from app.repositories.results import is_ot, upsert_result
from app.repositories.team_repository import TeamRepository

from app.repositories.predictions import (
    get_predictions,
    upsert_prediction,
    choice_to_string,
)
from app.session import Session
from app.utils import render

teams = TeamRepository()


@app.route("/debug/matches")
def matches():
    matches = [
        {
            "week": match.week,
            "home_team": teams.get_team_name(match.home_team),
            "away_team": teams.get_team_name(match.away_team),
            "start_time": match.start_time,
        }
        for match in app.session.query(Match).all()
    ]

    return render("/debug/matches.html", matches=matches)


@app.route("/week/<week>", methods=["GET", "POST"])
def week(week: int):
    user = Session(session).get_user()

    if request.method == "POST" and user:
        process_picks(request.form, user.id)

    matches = app.session.query(Match).filter_by(week=week).all()

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

    matches = [to_dict(match, predictions.get(match.id)) for match in matches]
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
        score_color=score_color
    )


def to_dict(match: Match, pick: str) -> dict:
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

            prediction = {"user_score": score, "user_win": win}

    return {
        **result,
        **prediction,
        "home_team": teams.get_team_name(match.home_team),
        "away_team": teams.get_team_name(match.away_team),
        "start_time": match.start_time,
        "id": match.id,
        "final": bool(match.result)
    }


def process_picks(picks: dict, user_id: int) -> None:
    for key, value in picks.items():
        if key.startswith("match_"):
            match_id = int(key[6:])
            upsert_prediction(match_id=match_id, user_id=user_id, choice=value)

    app.session.commit()

def points_color(points: int) -> str:
    return 'green' if points >= 0 else 'red'

def score_color(score: int, total: int) -> str:
    if total == 0:
        return 'unset'

    pct = score / total
    if pct > 0.6:
        return 'green'
    elif pct > 0.4:
        return 'orange'
    else:
        return 'red'