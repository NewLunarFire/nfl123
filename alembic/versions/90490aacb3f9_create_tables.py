"""create tables

Revision ID: 90490aacb3f9
Revises: 
Create Date: 2021-09-26 15:32:12.218785

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = "90490aacb3f9"
down_revision = None
branch_labels = None
depends_on = None

teams = [
    {"city_name": "Arizona", "team_name": "Cardinals"},
    {"city_name": "Atlanta", "team_name": "Falcons"},
    {"city_name": "Baltimore", "team_name": "Ravens"},
    {"city_name": "Buffalo", "team_name": "Bills"},
    {"city_name": "Carolina", "team_name": "Panthers"},
    {"city_name": "Chicago", "team_name": "Bears"},
    {"city_name": "Cincinnati", "team_name": "Bengals"},
    {"city_name": "Cleveland", "team_name": "Browns"},
    {"city_name": "Dallas", "team_name": "Cowboys"},
    {"city_name": "Denver", "team_name": "Broncos"},
    {"city_name": "Detroit", "team_name": "Lions"},
    {"city_name": "Green Bay", "team_name": "Packers"},
    {"city_name": "Houston", "team_name": "Texans"},
    {"city_name": "Indianapolis", "team_name": "Colts"},
    {"city_name": "Jacksonville", "team_name": "Jaguars"},
    {"city_name": "Kansas City", "team_name": "Chiefs"},
    {"city_name": "Las Vegas", "team_name": "Raiders"},
    {"city_name": "Los Angeles", "team_name": "Chargers"},
    {"city_name": "Los Angeles", "team_name": "Rams"},
    {"city_name": "Miami", "team_name": "Dolphins"},
    {"city_name": "Minnesota", "team_name": "Vikings"},
    {"city_name": "New York", "team_name": "Jets"},
    {"city_name": "New York", "team_name": "Giants"},
    {"city_name": "New Orleans", "team_name": "Saints"},
    {"city_name": "New England", "team_name": "Patriots"},
    {"city_name": "Philadelphia", "team_name": "Eagles"},
    {"city_name": "Pittsburgh", "team_name": "Steelers"},
    {"city_name": "San Francisco", "team_name": "49ers"},
    {"city_name": "Seattle", "team_name": "Seahawks"},
    {"city_name": "Tampa Bay", "team_name": "Buccaneers"},
    {"city_name": "Tennessee", "team_name": "Titans"},
    {"city_name": "Washington", "team_name": "Football Team"},
]


def upgrade():
    teams_table = op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("city_name", sa.String(50), nullable=False),
        sa.Column("team_name", sa.String(50), nullable=False),
    )
    op.bulk_insert(teams_table, teams)
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(50), nullable=False),
    )
    op.create_table(
        "user_stats",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("score", sa.Integer, nullable=False, default=0),
        sa.Column("good_picks", sa.Integer, nullable=False, default=0),
    )
    matches_table = op.create_table(
        "matches",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("week", sa.Integer, nullable=False),
        sa.Column("home_team", sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("away_team", sa.Integer, sa.ForeignKey("teams.id"), nullable=False),
        sa.Column("start_time", sa.DateTime, nullable=False, default=datetime.utcnow),
    )
    op.create_table(
        "match_results",
        sa.Column(
            "match_id", sa.Integer, sa.ForeignKey("matches.id"), primary_key=True
        ),
        sa.Column("result_type", sa.Integer, nullable=False),
        sa.Column("home_score", sa.Integer, nullable=False),
        sa.Column("away_score", sa.Integer, nullable=False),
    )
    op.create_table(
        "predictions",
        sa.Column(
            "match_id",
            sa.Integer,
            sa.ForeignKey("matches.id"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column(
            "user_id",
            sa.Integer,
            sa.ForeignKey("users.id"),
            nullable=False,
            primary_key=True,
        ),
        sa.Column("pick", sa.Integer, nullable=False),
    )

    matches = [
        {
            "week": 1,
            "home_team": x,
            "away_team": 33 - x,
            "start_time": datetime.utcnow(),
        }
        for x in range(1, 17)
    ]
    op.bulk_insert(matches_table, matches)

    pass


def downgrade():
    op.drop_table("teams")
    op.drop_table("users")
    op.drop_table("user_stats")
    op.drop_table("matches")
    op.drop_table("match_results")
    op.drop_table("predictions")
    pass
