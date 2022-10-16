from typing import Any, Dict, List

from app.database import Session
from app.models import MatchResult
from app.repositories.score import invalidate_cache

values = ["home", "away"]


def get_all_results() -> List[MatchResult]:
    return Session.query(MatchResult).all()


def get_results_for_matches(match_ids: List[int]):
    return Session.query(MatchResult).filter(MatchResult.match_id.in_(match_ids)).all()


def upsert_result(match_id: int, home_score: int, away_score: int, is_ot: bool) -> None:
    result_type = get_result_type(home_score, away_score, is_ot)

    match_result: MatchResult = (
        Session.query(MatchResult).filter_by(match_id=match_id).first()
    )

    if match_result:
        # Update
        match_result.home_score = home_score
        match_result.away_score = away_score
        match_result.result_type = result_type
    else:
        Session.add(
            MatchResult(
                match_id=match_id,
                home_score=home_score,
                away_score=away_score,
                result_type=result_type,
            )
        )

    invalidate_cache(match_id)


def get_result_type(home_score: int, away_score: int, is_ot: bool) -> int:
    # 0 = home win regulation
    # 1 = away win regulation
    # 2 = home win OT
    # 3 = away win OT
    # 4 = tie
    if home_score == away_score:
        return 4
    if home_score > away_score:
        return 2 if is_ot else 0

    return 3 if is_ot else 1


def result_is_ot(result_type: int):
    return result_type in {2, 3}


def result_to_dict(result: MatchResult) -> Dict[str, Any]:
    if not result:
        return {}

    return {
        "home_score": result.home_score,
        "away_score": result.away_score,
        "ot": result_is_ot(result.result_type),
    }
