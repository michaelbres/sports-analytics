"""
NFL Data Pipeline
Source: nfl_data_py (wraps nflfastR data hosted on GitHub — free, no key needed)

Run:  python -m pipelines.nfl_pipeline
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from database import SessionLocal, engine, Base
from models.nfl import NFLTeam, NFLPlayer, NFLPassingStats, NFLRushingStats, NFLReceivingStats
from config import NFL_SEASON

Base.metadata.create_all(bind=engine)


def run():
    db = SessionLocal()
    try:
        print(f"[NFL] Starting pipeline for {NFL_SEASON}...")
        _ingest_players(db)
        _ingest_seasonal_stats(db)
        print("[NFL] Done.")
    finally:
        db.close()


def _ingest_players(db):
    try:
        import nfl_data_py as nfl
        df = nfl.import_rosters([NFL_SEASON])
        for _, row in df.iterrows():
            player_id = str(row.get("player_id", ""))
            if not player_id:
                continue
            existing = db.query(NFLPlayer).filter_by(player_id=player_id).first()
            if existing:
                continue
            db.add(NFLPlayer(
                player_id=player_id,
                name=row.get("player_name", ""),
                position=row.get("position", ""),
                team=row.get("team", ""),
                age=int(row.get("age", 0) or 0),
                season=NFL_SEASON,
            ))
        db.commit()
        print(f"  [NFL] Players ingested: {len(df)}")
    except Exception as e:
        print(f"  [NFL] Player ingest error: {e}")


def _ingest_seasonal_stats(db):
    try:
        import nfl_data_py as nfl
        df = nfl.import_seasonal_data([NFL_SEASON])

        for _, row in df.iterrows():
            player_id = str(row.get("player_id", ""))
            if not player_id:
                continue

            position = str(row.get("position", ""))

            # Passing
            if float(row.get("attempts", 0) or 0) > 0:
                existing = db.query(NFLPassingStats).filter_by(player_id=player_id, season=NFL_SEASON).first()
                if not existing:
                    db.add(NFLPassingStats(
                        player_id=player_id,
                        season=NFL_SEASON,
                        games=int(row.get("games", 0) or 0),
                        attempts=int(row.get("attempts", 0) or 0),
                        completions=int(row.get("completions", 0) or 0),
                        completion_pct=float(row.get("completion_percentage", 0) or 0),
                        yards=int(row.get("passing_yards", 0) or 0),
                        touchdowns=int(row.get("passing_tds", 0) or 0),
                        interceptions=int(row.get("interceptions", 0) or 0),
                        yards_per_attempt=float(row.get("passing_yards_after_catch", 0) or 0),
                        passer_rating=float(row.get("pacr", 0) or 0),
                        epa_per_dropback=float(row.get("passing_epa", 0) or 0),
                        cpoe=float(row.get("cpoe", 0) or 0),
                        air_yards=float(row.get("passing_air_yards", 0) or 0),
                        dakota=float(row.get("dakota", 0) or 0),
                    ))

            # Rushing
            if float(row.get("carries", 0) or 0) > 0:
                existing = db.query(NFLRushingStats).filter_by(player_id=player_id, season=NFL_SEASON).first()
                if not existing:
                    db.add(NFLRushingStats(
                        player_id=player_id,
                        season=NFL_SEASON,
                        games=int(row.get("games", 0) or 0),
                        carries=int(row.get("carries", 0) or 0),
                        yards=int(row.get("rushing_yards", 0) or 0),
                        yards_per_carry=float(row.get("rushing_yards_per_attempt", 0) or 0),
                        touchdowns=int(row.get("rushing_tds", 0) or 0),
                        fumbles=int(row.get("rushing_fumbles", 0) or 0),
                        epa_per_rush=float(row.get("rushing_epa", 0) or 0),
                        success_rate=float(row.get("rushing_first_downs", 0) or 0),
                    ))

            # Receiving
            if float(row.get("targets", 0) or 0) > 0:
                existing = db.query(NFLReceivingStats).filter_by(player_id=player_id, season=NFL_SEASON).first()
                if not existing:
                    db.add(NFLReceivingStats(
                        player_id=player_id,
                        season=NFL_SEASON,
                        games=int(row.get("games", 0) or 0),
                        targets=int(row.get("targets", 0) or 0),
                        receptions=int(row.get("receptions", 0) or 0),
                        yards=int(row.get("receiving_yards", 0) or 0),
                        touchdowns=int(row.get("receiving_tds", 0) or 0),
                        yards_per_reception=float(row.get("receiving_yards_per_reception", 0) or 0),
                        catch_rate=float(row.get("target_share", 0) or 0),
                        epa_per_target=float(row.get("receiving_epa", 0) or 0),
                        air_yards=int(row.get("receiving_air_yards", 0) or 0),
                        racr=float(row.get("racr", 0) or 0),
                        target_share=float(row.get("target_share", 0) or 0),
                        adot=float(row.get("air_yards_share", 0) or 0),
                        wopr=float(row.get("wopr", 0) or 0),
                    ))

        db.commit()
        print(f"  [NFL] Seasonal stats ingested: {len(df)} rows")
    except Exception as e:
        print(f"  [NFL] Seasonal stats error: {e}")


if __name__ == "__main__":
    run()
