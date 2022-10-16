from dataclasses import dataclass
from typing import Tuple

from app.logger import logger
from app.models import Match, User, Week
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
        prediction.match_id: choice_to_string(prediction.pick)
        for prediction in get_predictions(
            match_ids=[match.id for match in matches], user_id=user.id
        )
    }

    points_total = 0
    win_total = 0
    total_matches = sum(bool(match.result) for match in matches)
    for match in matches:
        (points, win) = match_user_result(match=match, pick=predictions.get(match.id))
        points_total += points
        win_total += win

    return Score(points=points_total, score=win_total, total_matches=total_matches)


def match_user_result(match: Match, pick: str) -> Tuple[int, bool]:
    if not match.result:
        return (0, False)

    if pick:
        if pick == "home":
            return (
                match.result.home_score - match.result.away_score,
                match.result.home_score >= match.result.away_score,
            )

        return (
            match.result.away_score - match.result.home_score,
            match.result.away_score >= match.result.home_score,
        )

    return (-abs(match.result.home_score - match.result.away_score), False)
