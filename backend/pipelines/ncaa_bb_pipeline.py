"""
NCAA Basketball Data Pipeline
Source: ESPN unofficial API (no key needed)

Run:  python -m pipelines.ncaa_bb_pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
from database import SessionLocal, engine, Base
from models.ncaa_bb import NCAABBTeam, NCAABBTeamStats
from config import NCAA_BB_SEASON

Base.metadata.create_all(bind=engine)

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball"


def run():
    db = SessionLocal()
    try:
        print(f"[NCAA BB] Starting pipeline for {NCAA_BB_SEASON}...")
        _ingest_teams(db)
        _ingest_team_stats(db)
        print("[NCAA BB] Done.")
    finally:
        db.close()


def _ingest_teams(db):
    try:
        # ESPN groups by conference — pull top conferences
        conferences = [
            ("acc", "ACC"), ("big-12", "Big 12"), ("big-ten", "Big Ten"),
            ("sec", "SEC"), ("pac-12", "Pac-12"), ("big-east", "Big East"),
            ("american", "American"), ("mountain-west", "Mountain West"),
            ("wac", "WAC"), ("cusa", "C-USA"),
        ]
        count = 0
        for conf_slug, conf_name in conferences:
            resp = requests.get(
                f"{ESPN_BASE}/teams",
                params={"limit": 50, "groups": conf_slug},
                timeout=10,
            )
            if resp.status_code != 200:
                continue
            teams = resp.json().get("sports", [{}])[0].get("leagues", [{}])[0].get("teams", [])
            for t in teams:
                team = t.get("team", {})
                team_id = str(team.get("id", ""))
                if not team_id:
                    continue
                existing = db.query(NCAABBTeam).filter_by(team_id=team_id, season=NCAA_BB_SEASON).first()
                if not existing:
                    db.add(NCAABBTeam(
                        team_id=team_id,
                        name=team.get("displayName", ""),
                        conference=conf_name,
                        season=NCAA_BB_SEASON,
                    ))
                    count += 1
        db.commit()
        print(f"  [NCAA BB] Teams ingested: {count}")
    except Exception as e:
        print(f"  [NCAA BB] Teams error: {e}")


def _ingest_team_stats(db):
    """Pull team scoring/efficiency stats from ESPN scoreboard."""
    try:
        resp = requests.get(
            f"{ESPN_BASE}/standings",
            params={"season": NCAA_BB_SEASON.replace("-", "")[:4]},
            timeout=10,
        )
        if resp.status_code != 200:
            print(f"  [NCAA BB] Standings HTTP {resp.status_code}")
            return
        # ESPN standings structure varies — parse what's available
        groups = resp.json().get("children", [])
        count = 0
        for group in groups:
            for entry in group.get("standings", {}).get("entries", []):
                team_id = str(entry.get("team", {}).get("id", ""))
                if not team_id:
                    continue
                stats = {s["name"]: s.get("value", 0) for s in entry.get("stats", [])}
                existing = db.query(NCAABBTeamStats).filter_by(team_id=team_id, season=NCAA_BB_SEASON).first()
                if not existing:
                    db.add(NCAABBTeamStats(
                        team_id=team_id,
                        season=NCAA_BB_SEASON,
                        wins=int(stats.get("wins", 0) or 0),
                        losses=int(stats.get("losses", 0) or 0),
                        points_per_game=float(stats.get("pointsFor", 0) or 0),
                        points_allowed=float(stats.get("pointsAgainst", 0) or 0),
                    ))
                    count += 1
        db.commit()
        print(f"  [NCAA BB] Team stats ingested: {count}")
    except Exception as e:
        print(f"  [NCAA BB] Team stats error: {e}")


if __name__ == "__main__":
    run()
