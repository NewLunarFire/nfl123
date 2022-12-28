from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Tuple

from flask import Blueprint, abort, redirect, request

from app.authentication import authenticated
from app.database import Session
from app.enums.week_type import WeekType
from app.models import Match, MatchResult, User
from app.repositories.match import get_matches_for_team, get_matches_for_week
from app.repositories.predictions import (
    choice_to_string,
    get_predictions,
    get_predictions_for_match,
    is_game_started,
    upsert_prediction,
)
from app.repositories.results import result_is_ot
from app.repositories.scoreboard import get_scoreboard_for_match
from app.repositories.team_repository import TeamInfo, TeamRepository
from app.repositories.user import get_all_users
from app.repositories.week import get_all_weeks_in_year, get_current_week, get_week
from app.utils.rendering import render
from app.utils.time import get_request_time

match_blueprint = Blueprint("match", __name__)

teams = TeamRepository()


@dataclass
class MatchUserResult:
    score: int
    win: bool


@dataclass
class MatchResultInfo:
    home_score: int
    away_score: int
    is_ot: bool


@dataclass
class MatchInfo:
    id: int
    home_team: TeamInfo
    home_team_record: Tuple[int, int, int]
    away_team: TeamInfo
    away_team_record: Tuple[int, int, int]
    start_time: datetime

    is_locked: bool
    result: MatchResultInfo

    user_pick: str
    user_result: MatchUserResult

    other_picks_home: List[str]
    other_picks_away: List[str]

    scoreboard: Dict

    def is_final(self) -> bool:
        return bool(self.result)

    def get_user_score(self) -> int:
        return self.user_result.score if self.user_result else 0

    def get_user_win(self) -> bool:
        return self.user_result.win if self.user_result else False

    def has_user_selected(self) -> bool:
        return bool(self.user_pick)


@match_blueprint.route("/week")
@authenticated(with_user_param=False)
def default_week():
    current_week = get_current_week(datetime.now())
    return redirect(f"week/{current_week.display_name}")


@match_blueprint.route("/week/<week_name>", methods=["GET", "POST"])
@authenticated()
def week_matches(user: User, week_name: str):
    request_time = get_request_time()
    week = get_week(name=week_name, year=2022)

    if not week:
        abort(404)

    save_requested = request.method == "POST"
    total_requested, total_saved = 0, 0
    if save_requested:
        total_requested, total_saved = process_picks(
            request.form, user.id, request_time
        )

    matches = get_matches_for_week(week=week.id)

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

    users = get_all_users()
    matches = [
        to_match_info(match, predictions.get(match.id), users=users)
        for match in matches
    ]
    points = sum(match.get_user_score() for match in matches)
    score = sum(match.get_user_win() for match in matches)
    total_matches = sum(match.is_final() for match in matches)
    total_picks = sum(bool(match.user_pick) for match in matches)

    return render(
        "week.html",
        weeks=get_all_weeks_in_year(year=2022),
        week=week,
        matches=matches,
        predictions=predictions,
        points=points,
        score=score,
        total_matches=total_matches,
        total_picks=total_picks,
        save_requested=save_requested,
        total_requested=total_requested,
        total_saved=total_saved,
    )


def to_match_info(match: Match, pick: str, users: List[User]) -> MatchInfo:
    result = None
    user_dict = {user.id: user.name for user in users}

    if match.result:
        result = MatchResultInfo(
            home_score=match.result.home_score,
            away_score=match.result.away_score,
            is_ot=result_is_ot(match.result.result_type),
        )

    is_locked = is_game_started(request_time=get_request_time(), match=match)
    other_picks_home = []
    other_picks_away = []

    if is_locked:
        for prediction in get_predictions_for_match(match_id=match.id):
            name = user_dict[prediction.user_id]
            (other_picks_away if prediction.pick else other_picks_home).append(name)

    return MatchInfo(
        id=match.id,
        home_team=teams.get_team_info(match.home_team),
        home_team_record=get_team_record(team_id=match.home_team),
        away_team=teams.get_team_info(match.away_team),
        away_team_record=get_team_record(team_id=match.away_team),
        start_time=match.start_time,
        is_locked=is_locked,
        result=result,
        user_pick=pick,
        user_result=match_user_result(match, pick),
        other_picks_away=other_picks_away,
        other_picks_home=other_picks_home,
        scoreboard=get_scoreboard_for_match(match.id),
    )


def match_user_result(match: Match, pick: str):
    if not match.result:
        return None

    if pick:
        if pick == "home":
            return MatchUserResult(
                score=match.result.home_score - match.result.away_score,
                win=match.result.home_score >= match.result.away_score,
            )

        return MatchUserResult(
            score=match.result.away_score - match.result.home_score,
            win=match.result.away_score >= match.result.home_score,
        )

    return MatchUserResult(
        score=-abs(match.result.home_score - match.result.away_score), win=False
    )


def get_team_record(team_id: int):
    matches = get_matches_for_team(team_id=team_id)
    win = 0
    loss = 0
    tie = 0

    for match in matches:
        if match.result and match.week_rel.type in [WeekType.season, WeekType.playoffs]:
            is_home = match.home_team == team_id
            result: MatchResult = match.result

            is_win: bool
            is_loss: bool
            is_tie: bool

            if is_home:
                is_win = result.home_score > result.away_score
                is_loss = result.home_score < result.away_score
                is_tie = result.home_score == result.away_score

            else:
                is_win = result.away_score > result.home_score
                is_loss = result.away_score < result.home_score
                is_tie = result.away_score == result.home_score

            if is_win:
                win = win + 1
            elif is_loss:
                loss = loss + 1
            elif is_tie:
                tie = tie + 1

    return (win, loss, tie)


def process_picks(picks: dict, user_id: int, request_time: datetime) -> (int, int):
    total_requested = 0
    total_saved = 0

    for key, value in picks.items():
        if key.startswith("match_"):
            match_id = int(key[6:])
            total_requested += 1
            total_saved += upsert_prediction(
                match_id=match_id,
                user_id=user_id,
                choice=value,
                request_time=request_time,
            )

    Session.commit()
    return (total_requested, total_saved)
