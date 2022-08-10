from collections import namedtuple
from app import app
from app.models import Match, Prediction, User
from app.utils import render
from app.repositories.user import get_all_users
from app.repositories.match import get_all_matches
from app.repositories.predictions import get_predictions, choice_to_string

from operator import attrgetter
from typing import List, Dict, Tuple

UserScore = namedtuple("UserScore", "name points score")

@app.route("/standings")
def standings():
    users = get_all_users()
    matches = {match.id : match for match in get_all_matches() if match.result}
    total_matches = len(matches)

    user_scores = [calculate_points_for_user(matches, user) for user in users]

    user_scores.sort(key=attrgetter("points", "score"), reverse=True)
    return render("standings.html", users=user_scores, total_matches=total_matches)

def calculate_points_for_user(matches: List[Match], user: User) -> UserScore:
    total_score = 0
    total_points = 0
    predictions = {prediction.match_id : prediction for prediction in get_predictions(user_id=user.id, match_ids=matches.keys())}

    for (id, match) in matches.items():
        (win, points) = calculate_points_for_match(match=match, prediction=predictions.get(id))
        total_score += win
        total_points += points

    return UserScore(name=user.name, points=total_points, score=total_score)
    
def calculate_points_for_match(match: Match, prediction: Prediction) -> Tuple[bool, int]:
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
            