import sys
from pathlib import Path
import json
import os
import threading
from datetime import datetime, timedelta
from urllib.request import urlopen

if __name__ == "__main__":
    path_root = Path(__file__).parents[1]
    sys.path.append(str(path_root))
    print(sys.path)


from app.database import Session
from app.repositories.match import find_match, get_next_match
from app.repositories.results import upsert_result
from app.repositories.scoreboard import remove_match, update_match

teams = [
    "ARI",
    "ATL",
    "BAL",
    "BUF",
    "CAR",
    "CHI",
    "CIN",
    "CLE",
    "DAL",
    "DEN",
    "DET",
    "GB",
    "HOU",
    "IND",
    "JAX",
    "KC",
    "LV",
    "LAC",
    "LAR",
    "MIA",
    "MIN",
    "NYJ",
    "NYG",
    "NO",
    "NE",
    "PHI",
    "PIT",
    "SF",
    "SEA",
    "TB",
    "TEN",
    "WSH",
]


def __fetch_scoreboard():
    with urlopen(
        "https://site.web.api.espn.com/apis/v2/scoreboard/header?sport=football&league=nfl"
    ) as response:
        return response.read()


def __next_update_time(matches_in_progress: bool):
    if matches_in_progress:
        next_update = timedelta(minutes=5)  # Update again in 5 minutes
        print(
            f"Matches in progress, next update in {next_update} ({next_update.total_seconds()} seconds)"
        )
        return next_update.total_seconds()

    current_time = datetime.now()
    next_match = get_next_match(request_time=current_time)
    if not next_match:
        print("No future matches, do not update scoreboard again")
        return -1

    next_update = next_match.start_time - current_time
    next_seconds = next_update.total_seconds()
    print(
        f"Next match at {next_match.start_time}, next update in {next_update} ({next_seconds} seconds)"
    )
    return next_seconds


def __get_scoreboard() -> int:
    print("Updating scoreboard from ESPN")
    scoreboard = json.loads(__fetch_scoreboard())
    nfl = scoreboard["sports"][0]["leagues"][0]

    for event in nfl["events"]:
        # Status: pre, in, post
        if event["status"] in ["in", "post"]:
            away_team, home_team = event["shortName"].split(" @ ")
            away = teams.index(away_team) + 1
            home = teams.index(home_team) + 1
            start = datetime.strptime(event["date"], "%Y-%m-%dT%H:%M:%SZ")
            match = find_match(away_team=away, home_team=home, start_time=start)

            home_score = event["competitors"][0]["score"]
            away_score = event["competitors"][1]["score"]

            if event["status"] == "in":
                update_match(
                    match_id=match.id,
                    away_score=away_score,
                    home_score=home_score,
                    progress=event["summary"],
                )
            elif event["status"] == "post" and not match.result:
                remove_match(match.id)

                if not match.result:
                    is_ot = False
                    upsert_result(
                        match_id=match.id,
                        away_score=away_score,
                        home_score=home_score,
                        is_ot=is_ot,
                    )
                    Session.commit()  # Commit score updates

    return __next_update_time(
        matches_in_progress="in" in set(event["status"] for event in nfl["events"])
    )


def __periodic():
    threading.current_thread().name = "Timer"
    next_update = __get_scoreboard()
    if next_update > 0:
        threading.Timer(next_update, __periodic).start()


def start_updater():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        threading.Timer(0, __periodic).start()


if __name__ == "__main__":
    __get_scoreboard()
