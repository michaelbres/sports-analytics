from sqlalchemy import Column, Integer, String, Float
from database import Base


class NCAAFBPlayer(Base):
    __tablename__ = "ncaa_fb_players"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)  # CFBD player ID
    name = Column(String, index=True)
    position = Column(String, index=True)
    team = Column(String)
    conference = Column(String)
    season = Column(Integer)


class NCAAFBPassingStats(Base):
    __tablename__ = "ncaa_fb_passing"

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


class NCAAFBRushingStats(Base):
    __tablename__ = "ncaa_fb_rushing"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    games = Column(Integer)
    carries = Column(Integer)
    yards = Column(Integer)
    yards_per_carry = Column(Float)
    touchdowns = Column(Integer)
    long = Column(Integer)


class NCAAFBReceivingStats(Base):
    __tablename__ = "ncaa_fb_receiving"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(String, index=True)
    season = Column(Integer, index=True)
    games = Column(Integer)
    receptions = Column(Integer)
    targets = Column(Integer)
    yards = Column(Integer)
    yards_per_reception = Column(Float)
    touchdowns = Column(Integer)
    long = Column(Integer)
    # PFF-style (if available from CSV uploads)
    offense_grade = Column(Float)
    yards_per_route_run = Column(Float)
    drop_rate = Column(Float)
    contested_catch_rate = Column(Float)
    separation = Column(Float)
