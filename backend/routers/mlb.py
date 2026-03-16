from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.mlb import MLBTeam, MLBPlayer, MLBBattingStats, MLBPitchingStats

router = APIRouter()


@router.get("/teams")
def get_teams(season: int = Query(2025), db: Session = Depends(get_db)):
    return db.query(MLBTeam).filter(MLBTeam.season == season).all()


@router.get("/teams/{team_id}")
def get_team(team_id: str, season: int = Query(2025), db: Session = Depends(get_db)):
    return db.query(MLBTeam).filter(MLBTeam.team_id == team_id, MLBTeam.season == season).first()


@router.get("/players")
def get_players(
    season: int = Query(2025),
    position: Optional[str] = None,
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(MLBPlayer).filter(MLBPlayer.season == season)
    if position:
        q = q.filter(MLBPlayer.position == position)
    if team:
        q = q.filter(MLBPlayer.team == team)
    return q.all()


@router.get("/players/{player_id}")
def get_player(player_id: str, db: Session = Depends(get_db)):
    return db.query(MLBPlayer).filter(MLBPlayer.player_id == player_id).first()


@router.get("/batting")
def get_batting(
    season: int = Query(2025),
    min_pa: int = Query(50, description="Minimum plate appearances"),
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = (
        db.query(MLBBattingStats)
        .filter(MLBBattingStats.season == season, MLBBattingStats.plate_appearances >= min_pa)
    )
    return q.all()


@router.get("/pitching")
def get_pitching(
    season: int = Query(2025),
    min_ip: float = Query(10.0, description="Minimum innings pitched"),
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = (
        db.query(MLBPitchingStats)
        .filter(MLBPitchingStats.season == season, MLBPitchingStats.innings_pitched >= min_ip)
    )
    return q.all()
