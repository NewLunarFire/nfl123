from app import app
from app.authentication import authenticated
from app.utils import render
from app.models import Match, User
from app.repositories.team_repository import TeamRepository
from app.repositories.results import is_ot, upsert_result

from flask import request, redirect

teams = TeamRepository()


@app.route("/admin/result")
def results_redirect():
    return redirect("/admin/result/1")


@app.route("/admin/result/<week>", methods=["GET", "POST"])
@authenticated(require_admin=True)
def match_results(user: User, week: int):
    if request.method == "POST" and user:
        process_results(request.form)

    matches = [
        to_dict(match) for match in app.session.query(Match).filter_by(week=week).all()
    ]
    return render("admin/result.html", week=week, matches=matches)


def to_dict(match: Match) -> dict:
    result = {}

    if match.result:
        result = {
            "home_score": match.result.home_score,
            "away_score": match.result.away_score,
            "ot": is_ot(match.result.result_type),
        }

    return {
        **result,
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
            i1 = key.index("_")
            i2 = key.index("_", i1 + 1)

            match_id = int(key[i1 + 1 : i2])
            type = key[i2 + 1 :]
            res = results.get(match_id, {"ot": False})

            if type == "home":
                res["home"] = int(value)
            elif type == "away":
                res["away"] = int(value)
            elif type == "ot":
                res["ot"] = True
            else:
                continue

            results[match_id] = res

    print(results)
    for match_id, result in results.items():
        upsert_result(
            match_id=match_id,
            home_score=result["home"],
            away_score=result["away"],
            is_ot=result["ot"],
        )

    app.session.commit()
