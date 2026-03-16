"""
MLB Data Pipeline
Sources:
  - pybaseball: Statcast, batting stats, pitching stats (scrapes Baseball Savant & FanGraphs)
  - MLB Stats API: teams, rosters, standings (official, free)

Run:  python -m pipelines.mlb_pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal, engine, Base
from models.mlb import MLBTeam, MLBPlayer, MLBBattingStats, MLBPitchingStats
from config import MLB_SEASON

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        print(f"[MLB] Starting pipeline for {MLB_SEASON}...")
        _ingest_teams(db)
        _ingest_batting(db)
        _ingest_pitching(db)
        print("[MLB] Done.")
    finally:
        db.close()


def _ingest_teams(db):
    """Pull team stats from MLB Stats API."""
    import requests
    url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1&season={MLB_SEASON}"
    resp = requests.get(url, timeout=10)
    teams = resp.json().get("teams", [])
    for t in teams:
        team_id = str(t["id"])
        existing = db.query(MLBTeam).filter_by(team_id=team_id, season=MLB_SEASON).first()
        if not existing:
            db.add(MLBTeam(
                team_id=team_id,
                name=t.get("name"),
                abbreviation=t.get("abbreviation"),
                division=t.get("division", {}).get("name"),
                league=t.get("league", {}).get("name"),
                season=MLB_SEASON,
            ))
    db.commit()
    print(f"  [MLB] Teams ingested: {len(teams)}")


def _ingest_batting(db):
    """Pull batting stats via pybaseball (Baseball Savant / FanGraphs)."""
    try:
        import pybaseball
        pybaseball.cache.enable()
        df = pybaseball.batting_stats(MLB_SEASON, qual=50)
        for _, row in df.iterrows():
            player_id = str(row.get("IDfg", row.get("playerid", "")))
            if not player_id:
                continue
            existing = db.query(MLBBattingStats).filter_by(player_id=player_id, season=MLB_SEASON).first()
            if existing:
                continue
            db.add(MLBBattingStats(
                player_id=player_id,
                season=MLB_SEASON,
                games=int(row.get("G", 0) or 0),
                plate_appearances=int(row.get("PA", 0) or 0),
                at_bats=int(row.get("AB", 0) or 0),
                hits=int(row.get("H", 0) or 0),
                doubles=int(row.get("2B", 0) or 0),
                triples=int(row.get("3B", 0) or 0),
                home_runs=int(row.get("HR", 0) or 0),
                rbi=int(row.get("RBI", 0) or 0),
                runs=int(row.get("R", 0) or 0),
                stolen_bases=int(row.get("SB", 0) or 0),
                walks=int(row.get("BB", 0) or 0),
                strikeouts=int(row.get("SO", 0) or 0),
                batting_avg=float(row.get("AVG", 0) or 0),
                obp=float(row.get("OBP", 0) or 0),
                slg=float(row.get("SLG", 0) or 0),
                ops=float(row.get("OPS", 0) or 0),
                xba=float(row.get("xAVG", 0) or 0),
                xslg=float(row.get("xSLG", 0) or 0),
                xwoba=float(row.get("xwOBA", 0) or 0),
                barrel_pct=float(row.get("Barrel%", 0) or 0),
                hard_hit_pct=float(row.get("HardHit%", 0) or 0),
                exit_velocity=float(row.get("EV", 0) or 0),
                launch_angle=float(row.get("LA", 0) or 0),
                sprint_speed=float(row.get("Sprint Speed", 0) or 0),
            ))
        db.commit()
        print(f"  [MLB] Batting rows ingested: {len(df)}")
    except Exception as e:
        print(f"  [MLB] Batting ingest error: {e}")


def _ingest_pitching(db):
    """Pull pitching stats via pybaseball."""
    try:
        import pybaseball
        df = pybaseball.pitching_stats(MLB_SEASON, qual=10)
        for _, row in df.iterrows():
            player_id = str(row.get("IDfg", row.get("playerid", "")))
            if not player_id:
                continue
            existing = db.query(MLBPitchingStats).filter_by(player_id=player_id, season=MLB_SEASON).first()
            if existing:
                continue
            db.add(MLBPitchingStats(
                player_id=player_id,
                season=MLB_SEASON,
                games=int(row.get("G", 0) or 0),
                games_started=int(row.get("GS", 0) or 0),
                innings_pitched=float(row.get("IP", 0) or 0),
                wins=int(row.get("W", 0) or 0),
                losses=int(row.get("L", 0) or 0),
                saves=int(row.get("SV", 0) or 0),
                era=float(row.get("ERA", 0) or 0),
                whip=float(row.get("WHIP", 0) or 0),
                strikeouts=int(row.get("SO", 0) or 0),
                walks=int(row.get("BB", 0) or 0),
                k_per_9=float(row.get("K/9", 0) or 0),
                bb_per_9=float(row.get("BB/9", 0) or 0),
                fip=float(row.get("FIP", 0) or 0),
                xera=float(row.get("xERA", 0) or 0),
                xfip=float(row.get("xFIP", 0) or 0),
                barrel_pct_against=float(row.get("Barrel%", 0) or 0),
                hard_hit_pct_against=float(row.get("HardHit%", 0) or 0),
            ))
        db.commit()
        print(f"  [MLB] Pitching rows ingested: {len(df)}")
    except Exception as e:
        print(f"  [MLB] Pitching ingest error: {e}")


if __name__ == "__main__":
    run()
