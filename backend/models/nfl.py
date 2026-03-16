from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base


class NFLTeam(Base):
    __tablename__ = "nfl_teams"

    id = Column(Integer, primary_key=True, index=True)
    team_abbr = Column(String, unique=True, index=True)
    name = Column(String)
    conference = Column(String)
    division = Column(String)
    season = Column(Integer)

    # Offense
    points_per_game = Column(Float)
    yards_per_game = Column(Float)
    pass_yards_per_game = Column(Float)
    rush_yards_per_game = Column(Float)
    epa_per_play = Column(Float)
    success_rate = Column(Float)

    # Defense
    points_allowed_per_game = Column(Float)
    yards_allowed_per_game = Column(Float)
    def_epa_per_play = Column(Float)


class NFLPlayer(Base):
    __tablename__ = "nfl_players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, unique=True, index=True)  # gsis_id
    name = Column(String, index=True)
    position = Column(String, index=True)
    team = Column(String)
    age = Column(Integer)
    season = Column(Integer)


class NFLPassingStats(Base):
    __tablename__ = "nfl_passing"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    games = Column(Integer)
    attempts = Column(Integer)
    completions = Column(Integer)
    completion_pct = Column(Float)
    yards = Column(Integer)
    touchdowns = Column(Integer)
    interceptions = Column(Integer)
    yards_per_attempt = Column(Float)
    passer_rating = Column(Float)
    # Advanced (nflfastR)
    epa_per_dropback = Column(Float)
    cpoe = Column(Float)  # completion pct over expected
    air_yards = Column(Float)
    dakota = Column(Float)  # composite metric


class NFLRushingStats(Base):
    __tablename__ = "nfl_rushing"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    games = Column(Integer)
    carries = Column(Integer)
    yards = Column(Integer)
    yards_per_carry = Column(Float)
    touchdowns = Column(Integer)
    fumbles = Column(Integer)
    # Advanced
    epa_per_rush = Column(Float)
    success_rate = Column(Float)
    yards_after_contact = Column(Float)
    broken_tackles = Column(Integer)


class NFLReceivingStats(Base):
    __tablename__ = "nfl_receiving"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    games = Column(Integer)
    targets = Column(Integer)
    receptions = Column(Integer)
    yards = Column(Integer)
    touchdowns = Column(Integer)
    yards_per_reception = Column(Float)
    catch_rate = Column(Float)
    # Advanced
    epa_per_target = Column(Float)
    air_yards = Column(Integer)
    racr = Column(Float)  # receiver air conversion ratio
    target_share = Column(Float)
    adot = Column(Float)  # avg depth of target
    separation = Column(Float)
    wopr = Column(Float)  # weighted opportunity rating
