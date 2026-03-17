from sqlalchemy import Column, Integer, String, Float
from database import Base


class MLBTeam(Base):
    __tablename__ = "mlb_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(String, index=True)
    name = Column(String)
    abbreviation = Column(String)
    division = Column(String)
    league = Column(String)
    season = Column(Integer, index=True)

    # Team batting
    runs = Column(Float)
    home_runs = Column(Float)
    batting_avg = Column(Float)
    obp = Column(Float)
    slg = Column(Float)
    ops = Column(Float)

    # Team pitching
    era = Column(Float)
    whip = Column(Float)
    k_per_9 = Column(Float)
    fip = Column(Float)


class MLBBattingStats(Base):
    __tablename__ = "mlb_batting"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    name = Column(String, index=True)
    team = Column(String)
    position = Column(String)
    age = Column(Integer)
    games = Column(Integer)
    plate_appearances = Column(Integer)
    at_bats = Column(Integer)
    hits = Column(Integer)
    doubles = Column(Integer)
    triples = Column(Integer)
    home_runs = Column(Integer)
    rbi = Column(Integer)
    runs = Column(Integer)
    stolen_bases = Column(Integer)
    walks = Column(Integer)
    strikeouts = Column(Integer)
    batting_avg = Column(Float)
    obp = Column(Float)
    slg = Column(Float)
    ops = Column(Float)
    wrc_plus = Column(Float)
    war = Column(Float)
    # Statcast
    xba = Column(Float)
    xslg = Column(Float)
    xwoba = Column(Float)
    barrel_pct = Column(Float)
    hard_hit_pct = Column(Float)
    launch_angle = Column(Float)
    exit_velocity = Column(Float)
    sprint_speed = Column(Float)


class MLBPitchingStats(Base):
    __tablename__ = "mlb_pitching"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    name = Column(String, index=True)
    team = Column(String)
    age = Column(Integer)
    games = Column(Integer)
    games_started = Column(Integer)
    innings_pitched = Column(Float)
    wins = Column(Integer)
    losses = Column(Integer)
    saves = Column(Integer)
    era = Column(Float)
    whip = Column(Float)
    strikeouts = Column(Integer)
    walks = Column(Integer)
    k_per_9 = Column(Float)
    bb_per_9 = Column(Float)
    k_bb = Column(Float)
    fip = Column(Float)
    war = Column(Float)
    # Statcast
    xera = Column(Float)
    xfip = Column(Float)
    barrel_pct_against = Column(Float)
    hard_hit_pct_against = Column(Float)
    avg_velocity = Column(Float)
