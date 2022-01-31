from black import re
from app import app
from app.models import Match
from flask import render_template, session, request
from app.repositories.team_repository import TeamRepository
from app.repositories.predictions import (
    get_predictions,
    upsert_prediction,
    choice_to_string,
)

teams = TeamRepository()


@app.route("/matches")
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

    return render_template("matches.html", matches=matches, name=session["user_name"])


@app.route("/week/<week>", methods=["GET", "POST"])
def week(week: int):
    user_id = int(session["user_id"])
    if request.method == "POST":
        process_picks(request.form, user_id)

    matches = [
        {
            "home_team": teams.get_team_name(match.home_team),
            "away_team": teams.get_team_name(match.away_team),
            "start_time": match.start_time,
            "id": match.id,
        }
        for match in app.session.query(Match).filter_by(week=week).all()
    ]

    predictions = {}
    for prediction in get_predictions(
        match_ids=[match["id"] for match in matches], user_id=user_id
    ):
        predictions[prediction.match_id] = choice_to_string(prediction.pick)

    return render_template(
        "week.html",
        week=week,
        matches=matches,
        name=session["user_name"],
        predictions=predictions,
    )


def process_picks(picks: dict, user_id: int) -> None:
    for key, value in picks.items():
        if key.startswith("match_"):
            match_id = int(key[6:])
            upsert_prediction(match_id=match_id, user_id=user_id, choice=value)

    app.session.commit()
