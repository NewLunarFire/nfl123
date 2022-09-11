matches = {}


def update_match(match_id: int, away_score: int, home_score: int, progress: str):
    matches[match_id] = {
        "away_score": away_score,
        "home_score": home_score,
        "progress": progress,
    }


def remove_match(match_id: int):
    del matches[match_id]


def get_scoreboard_for_match(match_id: int):
    return matches.get(match_id)
