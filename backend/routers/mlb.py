from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.mlb import MLBTeam, MLBBattingStats, MLBPitchingStats

router = APIRouter()


@router.get("/teams")
def get_teams(season: int = Query(2025), db: Session = Depends(get_db)):
    return [r.to_dict() for r in db.query(MLBTeam).filter(MLBTeam.season == season).all()]


@router.get("/teams/{team_id}")
def get_team(team_id: str, season: int = Query(2025), db: Session = Depends(get_db)):
    r = db.query(MLBTeam).filter(MLBTeam.team_id == team_id, MLBTeam.season == season).first()
    return r.to_dict() if r else None


@router.get("/batting")
def get_batting(
    season: int = Query(2025),
    min_pa: int = Query(0, description="Minimum plate appearances"),
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(MLBBattingStats).filter(
        MLBBattingStats.season == season,
        MLBBattingStats.plate_appearances >= min_pa,
    )
    if team:
        q = q.filter(MLBBattingStats.team == team)
    return [r.to_dict() for r in q.all()]


@router.get("/pitching")
def get_pitching(
    season: int = Query(2025),
    min_ip: float = Query(0, description="Minimum innings pitched"),
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(MLBPitchingStats).filter(
        MLBPitchingStats.season == season,
        MLBPitchingStats.innings_pitched >= min_ip,
    )
    if team:
        q = q.filter(MLBPitchingStats.team == team)
    return [r.to_dict() for r in q.all()]
