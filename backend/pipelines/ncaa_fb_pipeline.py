"""
NCAA Football Data Pipeline
Source: College Football Data API (CFBD) — free tier, requires free API key
Sign up: https://collegefootballdata.com/key

Run:  python -m pipelines.ncaa_fb_pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
from database import SessionLocal, engine, Base
from models.ncaa_fb import NCAAFBPlayer, NCAAFBPassingStats, NCAAFBRushingStats, NCAAFBReceivingStats
from config import CFBD_API_KEY, NCAA_FB_SEASON

Base.metadata.create_all(bind=engine)

BASE_URL = "https://api.collegefootballdata.com"
HEADERS = {"Authorization": f"Bearer {CFBD_API_KEY}"}


def _get(endpoint, params=None):
    resp = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, params=params, timeout=15)
    resp.raise_for_status()
    return resp.json()


def run():
    if not CFBD_API_KEY:
        print("[NCAA FB] ERROR: CFBD_API_KEY not set in .env")
        print("  Get a free key at: https://collegefootballdata.com/key")
        return

    db = SessionLocal()
    try:
        print(f"[NCAA FB] Starting pipeline for {NCAA_FB_SEASON}...")
        _ingest_passing(db)
        _ingest_rushing(db)
        _ingest_receiving(db)
        print("[NCAA FB] Done.")
    finally:
        db.close()


def _upsert_player(db, player_id, name, position, team, conference, season):
    existing = db.query(NCAAFBPlayer).filter_by(player_id=player_id, season=season).first()
    if not existing:
        db.add(NCAAFBPlayer(
            player_id=player_id,
            name=name,
            position=position,
            team=team,
            conference=conference,
            season=season,
        ))


def _ingest_passing(db):
    try:
        data = _get("/stats/player/season", {"year": NCAA_FB_SEASON, "category": "passing"})
        count = 0
        for row in data:
            player_id = str(row.get("playerId", ""))
            if not player_id:
                continue
            _upsert_player(db, player_id, row.get("player", ""), "QB",
                           row.get("team", ""), row.get("conference", ""), NCAA_FB_SEASON)
            existing = db.query(NCAAFBPassingStats).filter_by(player_id=player_id, season=NCAA_FB_SEASON).first()
            if not existing:
                stat = row.get("stat", 0) or 0
                db.add(NCAAFBPassingStats(
                    player_id=player_id,
                    season=NCAA_FB_SEASON,
                    yards=int(stat) if row.get("statType") == "YDS" else 0,
                ))
                count += 1
        db.commit()
        print(f"  [NCAA FB] Passing rows: {count}")
    except Exception as e:
        print(f"  [NCAA FB] Passing error: {e}")


def _ingest_rushing(db):
    try:
        data = _get("/stats/player/season", {"year": NCAA_FB_SEASON, "category": "rushing"})
        count = 0
        for row in data:
            player_id = str(row.get("playerId", ""))
            if not player_id:
                continue
            _upsert_player(db, player_id, row.get("player", ""), "RB",
                           row.get("team", ""), row.get("conference", ""), NCAA_FB_SEASON)
            existing = db.query(NCAAFBRushingStats).filter_by(player_id=player_id, season=NCAA_FB_SEASON).first()
            if not existing:
                db.add(NCAAFBRushingStats(
                    player_id=player_id,
                    season=NCAA_FB_SEASON,
                    yards=int(row.get("stat", 0) or 0),
                ))
                count += 1
        db.commit()
        print(f"  [NCAA FB] Rushing rows: {count}")
    except Exception as e:
        print(f"  [NCAA FB] Rushing error: {e}")


def _ingest_receiving(db):
    try:
        data = _get("/stats/player/season", {"year": NCAA_FB_SEASON, "category": "receiving"})
        count = 0
        for row in data:
            player_id = str(row.get("playerId", ""))
            if not player_id:
                continue
            _upsert_player(db, player_id, row.get("player", ""), "WR",
                           row.get("team", ""), row.get("conference", ""), NCAA_FB_SEASON)
            existing = db.query(NCAAFBReceivingStats).filter_by(player_id=player_id, season=NCAA_FB_SEASON).first()
            if not existing:
                db.add(NCAAFBReceivingStats(
                    player_id=player_id,
                    season=NCAA_FB_SEASON,
                    yards=int(row.get("stat", 0) or 0),
                ))
                count += 1
        db.commit()
        print(f"  [NCAA FB] Receiving rows: {count}")
    except Exception as e:
        print(f"  [NCAA FB] Receiving error: {e}")


if __name__ == "__main__":
    run()
