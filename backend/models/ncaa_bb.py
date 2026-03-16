from sqlalchemy import Column, Integer, String, Float
from database import Base


class NCAABBTeam(Base):
    __tablename__ = "ncaa_bb_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    name = Column(String, index=True)
    conference = Column(String)
    season = Column(String)  # e.g. "2024-25"


class NCAABBTeamStats(Base):
    __tablename__ = "ncaa_bb_team_stats"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    season = Column(String, index=True)
    games = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)

    # Offense
    points_per_game = Column(Float)
    field_goal_pct = Column(Float)
    three_point_pct = Column(Float)
    free_throw_pct = Column(Float)
    offensive_rebounds = Column(Float)
    assists_per_game = Column(Float)
    turnovers_per_game = Column(Float)

    # Efficiency (KenPom-style)
    offensive_efficiency = Column(Float)   # points per 100 possessions
    defensive_efficiency = Column(Float)
    net_efficiency = Column(Float)
    tempo = Column(Float)                  # possessions per 40 min

    # Four Factors (Dean Oliver)
    efg_pct = Column(Float)               # effective FG%
    tov_rate = Column(Float)              # turnover rate
    orb_rate = Column(Float)              # offensive rebound rate
    ft_rate = Column(Float)               # free throw rate

    # Defense
    points_allowed = Column(Float)
    opp_field_goal_pct = Column(Float)
    blocks_per_game = Column(Float)
    steals_per_game = Column(Float)
