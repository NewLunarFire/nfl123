from dataclasses import dataclass
from typing import Tuple

from app.logger import logger
from app.models import Match, Prediction, User, Week, WeekType
from app.repositories.match import get_match, get_matches_for_week
from app.repositories.predictions import choice_to_string, get_predictions


@dataclass
class Score:
    points: int
    score: int
    total_matches: int


score_cache = {}


def get_week_score(user: User, week: Week) -> Score:
    key = (user.id, week.id)
    if key in score_cache:
        logger.debug(f"Score for {user.name} week {week.display_name} in cache")
        return score_cache.get(key)

    logger.debug(f"Calculating score for {user.name} week {week.display_name}")
    score = calculate_week_score(user, week)

    score_cache[key] = score
    return score


def invalidate_cache(match_id: int):
    match = get_match(match_id)
    keys_to_delete = [key for key in score_cache if key[1] == match.week_rel.id]
    for key in keys_to_delete:
        logger.debug(f"Remove {key} from score cache")
        del score_cache[key]


def calculate_week_score(user: User, week: Week):
    matches = get_matches_for_week(week=week.id)
    predictions = {
        prediction.match_id: prediction
        for prediction in get_predictions(
            match_ids=[match.id for match in matches], user_id=user.id
        )
    }

    points_total = 0
    win_total = 0
    total_matches = sum(bool(match.result) for match in matches)
    for match in matches:
        (points, win) = match_user_result(
            match=match, prediction=predictions.get(match.id)
        )
        points_total += points
        win_total += win

    return Score(points=points_total, score=win_total, total_matches=total_matches)


def calculate_playoff_score(
    match: Match, user_prediction: Prediction
) -> Tuple[int, bool]:
    if not user_prediction:
        return (0, False)

    pick = choice_to_string(user_prediction.pick)
    points = user_prediction.points.points

    # Calculate if home team won using final score
    home_win = match.result.home_score > match.result.away_score
    # Determine if user wins his prediction based on his pick.
    win = home_win if pick == "home" else not home_win

    return (points if win else -points, win)


def match_user_result(match: Match, prediction: Prediction) -> Tuple[int, bool]:
    if not match.result:
        return (0, False)

    if match.week_rel.type == WeekType.playoffs:
        return calculate_playoff_score(match, prediction)

    if prediction:
        if prediction.pick == "home":
            return (
                match.result.home_score - match.result.away_score,
                match.result.home_score >= match.result.away_score,
            )

        return (
            match.result.away_score - match.result.home_score,
            match.result.away_score >= match.result.home_score,
        )

    return (-abs(match.result.home_score - match.result.away_score), False)
