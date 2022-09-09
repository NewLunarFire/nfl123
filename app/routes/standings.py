from collections import namedtuple
from datetime import datetime
from operator import attrgetter
from typing import List, Tuple

from flask import Blueprint, redirect, url_for

from app.authentication import authenticated
from app.models import Match, Prediction, User, WeekType
from app.repositories.match import get_matches_for_weeks
from app.repositories.predictions import choice_to_string, get_predictions
from app.repositories.user import get_all_users
from app.repositories.week import get_current_week, get_weeks_in_year_by_type
from app.utils.rendering import render

standings_blueprint = Blueprint("standings", __name__)
UserScore = namedtuple("UserScore", "name points score")


@standings_blueprint.route("/standings")
@authenticated(with_user_param=False)
def default_standings():
    week = get_current_week(datetime.now())
    return redirect(url_for("standings.standings", season_type=week.type.name))


@standings_blueprint.route("/standings/<season_type>")
@authenticated(with_user_param=False)
def standings(season_type: str):
    users = get_all_users()
    week_type = WeekType[season_type]
    weeks = get_weeks_in_year_by_type(week_type=week_type, year=2022)

    matches = {
        match.id: match
        for match in get_matches_for_weeks(weeks=[week.id for week in weeks])
        if match.result
    }
    total_matches = len(matches)

    user_scores = [calculate_points_for_user(matches, user) for user in users]

    user_scores.sort(key=attrgetter("points", "score"), reverse=True)
    return render(
        "standings.html",
        users=user_scores,
        total_matches=total_matches,
        week_type=season_type,
    )


def calculate_points_for_user(matches: List[Match], user: User) -> UserScore:
    total_score = 0
    total_points = 0
    predictions = {
        prediction.match_id: prediction
        for prediction in get_predictions(user_id=user.id, match_ids=matches.keys())
    }

    for (match_id, match) in matches.items():
        (win, points) = calculate_points_for_match(
            match=match, prediction=predictions.get(match_id)
        )
        total_score += win
        total_points += points

    return UserScore(name=user.name, points=total_points, score=total_score)


def calculate_points_for_match(
    match: Match, prediction: Prediction
) -> Tuple[bool, int]:
    points: int
    win: bool

    if prediction:
        pick = choice_to_string(prediction.pick)
        if pick == "home":
            points = match.result.home_score - match.result.away_score
            win = match.result.home_score >= match.result.away_score
        else:
            points = match.result.away_score - match.result.home_score
            win = match.result.away_score >= match.result.home_score
    else:
        points = -abs(match.result.home_score - match.result.away_score)
        win = False

    return (win, points)
