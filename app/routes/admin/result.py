from datetime import datetime

from flask import Blueprint, redirect, request

from app.authentication import authenticated
from app.database import Session
from app.models import Match, User
from app.repositories.results import result_to_dict, upsert_result
from app.repositories.team_repository import TeamRepository
from app.repositories.week import get_all_weeks_in_year, get_current_week, get_week
from app.utils.rendering import render

teams = TeamRepository()
result_blueprint = Blueprint("results", __name__)


@result_blueprint.route("/admin/result")
def results_redirect():
    current_week = get_current_week(datetime.now())
    return redirect(f"/admin/result/{current_week.display_name}")


@result_blueprint.route("/admin/result/<week_name>", methods=["GET", "POST"])
@authenticated(require_admin=True)
def match_results(user: User, week_name: str):
    week = get_week(name=week_name, year=2022)

    if request.method == "POST" and user:
        process_results(request.form)

    matches = [
        to_dict(match) for match in Session.query(Match).filter_by(week=week.id).all()
    ]

    return render(
        "admin/result.html",
        week=week,
        weeks=get_all_weeks_in_year(year=2022),
        matches=matches,
    )


def to_dict(match: Match) -> dict:
    return {
        **result_to_dict(match.result),
        "home_team": teams.get_team_name(match.home_team),
        "away_team": teams.get_team_name(match.away_team),
        "start_time": match.start_time,
        "id": match.id,
    }


def process_results(picks: dict) -> None:
    results = {}

    for key, value in picks.items():
        if not value:
            continue

        if key.startswith("match_"):
            underscore_1 = key.index("_")
            underscore_2 = key.index("_", underscore_1 + 1)

            match_id = int(key[underscore_1 + 1 : underscore_2])
            pick_type = key[underscore_2 + 1 :]
            res = results.get(match_id, {"ot": False})

            if pick_type == "home":
                res["home"] = int(value)
            elif pick_type == "away":
                res["away"] = int(value)
            elif pick_type == "ot":
                res["ot"] = True
            else:
                continue

            results[match_id] = res

    for match_id, result in results.items():
        upsert_result(
            match_id=match_id,
            home_score=result["home"],
            away_score=result["away"],
            is_ot=result["ot"],
        )

    Session.commit()
