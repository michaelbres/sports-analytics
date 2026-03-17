"""
MLB Data Pipeline
Sources:
  - pybaseball: batting_stats / pitching_stats (FanGraphs) + Statcast (Baseball Savant)
  - MLB Stats API: teams (official, free, no key)

Run:  python -m pipelines.mlb_pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import requests
from database import SessionLocal, engine, Base
from models.mlb import MLBTeam, MLBBattingStats, MLBPitchingStats
from config import MLB_SEASON

Base.metadata.create_all(bind=engine)


def _f(val, default=None):
    """Safe float conversion — returns None for NaN/None."""
    try:
        v = float(val)
        return None if (v != v) else v  # NaN check
    except (TypeError, ValueError):
        return default


def _i(val, default=None):
    """Safe int conversion."""
    try:
        return int(float(val))
    except (TypeError, ValueError):
        return default


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
    """Pull team list from official MLB Stats API."""
    try:
        url = f"https://statsapi.mlb.com/api/v1/teams?sportId=1&season={MLB_SEASON}"
        teams = requests.get(url, timeout=10).json().get("teams", [])
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
        print(f"  [MLB] Teams: {len(teams)}")
    except Exception as e:
        print(f"  [MLB] Teams error: {e}")


def _ingest_batting(db):
    """Pull batting leaderboard from FanGraphs via pybaseball."""
    try:
        import pybaseball
        pybaseball.cache.enable()
        df = pybaseball.batting_stats(MLB_SEASON, qual=50)
        print(f"  [MLB] Batting columns: {list(df.columns)}")

        # Wipe and re-insert for idempotency
        db.query(MLBBattingStats).filter_by(season=MLB_SEASON).delete()
        db.commit()

        added = 0
        for _, row in df.iterrows():
            player_id = str(row.get("IDfg") or row.get("playerid") or "")
            name = str(row.get("Name") or row.get("name") or "")
            if not player_id or not name:
                continue

            db.add(MLBBattingStats(
                player_id=player_id,
                season=MLB_SEASON,
                name=name,
                team=str(row.get("Team") or row.get("team") or ""),
                position=str(row.get("Pos") or row.get("pos") or ""),
                age=_i(row.get("Age")),
                games=_i(row.get("G")),
                plate_appearances=_i(row.get("PA")),
                at_bats=_i(row.get("AB")),
                hits=_i(row.get("H")),
                doubles=_i(row.get("2B")),
                triples=_i(row.get("3B")),
                home_runs=_i(row.get("HR")),
                rbi=_i(row.get("RBI")),
                runs=_i(row.get("R")),
                stolen_bases=_i(row.get("SB")),
                walks=_i(row.get("BB")),
                strikeouts=_i(row.get("SO")),
                batting_avg=_f(row.get("AVG")),
                obp=_f(row.get("OBP")),
                slg=_f(row.get("SLG")),
                ops=_f(row.get("OPS")),
                wrc_plus=_f(row.get("wRC+")),
                war=_f(row.get("WAR")),
                xba=_f(row.get("xAVG") or row.get("xBA")),
                xslg=_f(row.get("xSLG")),
                xwoba=_f(row.get("xwOBA")),
                barrel_pct=_f(row.get("Barrel%") or row.get("Barrels%")),
                hard_hit_pct=_f(row.get("HardHit%")),
                exit_velocity=_f(row.get("EV") or row.get("AvgEV")),
                launch_angle=_f(row.get("LA") or row.get("AvgLA")),
                sprint_speed=_f(row.get("Sprint Speed")),
            ))
            added += 1

        db.commit()
        print(f"  [MLB] Batting rows: {added}")
    except Exception as e:
        import traceback
        print(f"  [MLB] Batting error: {e}")
        traceback.print_exc()


def _ingest_pitching(db):
    """Pull pitching leaderboard from FanGraphs via pybaseball."""
    try:
        import pybaseball
        df = pybaseball.pitching_stats(MLB_SEASON, qual=10)
        print(f"  [MLB] Pitching columns: {list(df.columns)}")

        db.query(MLBPitchingStats).filter_by(season=MLB_SEASON).delete()
        db.commit()

        added = 0
        for _, row in df.iterrows():
            player_id = str(row.get("IDfg") or row.get("playerid") or "")
            name = str(row.get("Name") or row.get("name") or "")
            if not player_id or not name:
                continue

            db.add(MLBPitchingStats(
                player_id=player_id,
                season=MLB_SEASON,
                name=name,
                team=str(row.get("Team") or row.get("team") or ""),
                age=_i(row.get("Age")),
                games=_i(row.get("G")),
                games_started=_i(row.get("GS")),
                innings_pitched=_f(row.get("IP")),
                wins=_i(row.get("W")),
                losses=_i(row.get("L")),
                saves=_i(row.get("SV")),
                era=_f(row.get("ERA")),
                whip=_f(row.get("WHIP")),
                strikeouts=_i(row.get("SO") or row.get("K")),
                walks=_i(row.get("BB")),
                k_per_9=_f(row.get("K/9")),
                bb_per_9=_f(row.get("BB/9")),
                k_bb=_f(row.get("K/BB")),
                fip=_f(row.get("FIP")),
                war=_f(row.get("WAR")),
                xera=_f(row.get("xERA")),
                xfip=_f(row.get("xFIP")),
                barrel_pct_against=_f(row.get("Barrel%") or row.get("Barrels%")),
                hard_hit_pct_against=_f(row.get("HardHit%")),
                avg_velocity=_f(row.get("vFA (pi)") or row.get("FBv") or row.get("AvgVelo")),
            ))
            added += 1

        db.commit()
        print(f"  [MLB] Pitching rows: {added}")
    except Exception as e:
        import traceback
        print(f"  [MLB] Pitching error: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    run()
