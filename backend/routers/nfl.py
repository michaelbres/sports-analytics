from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.nfl import NFLTeam, NFLPlayer, NFLPassingStats, NFLRushingStats, NFLReceivingStats

router = APIRouter()


@router.get("/teams")
def get_teams(season: int = Query(2024), db: Session = Depends(get_db)):
    return db.query(NFLTeam).filter(NFLTeam.season == season).all()


@router.get("/teams/{team_abbr}")
def get_team(team_abbr: str, season: int = Query(2024), db: Session = Depends(get_db)):
    return db.query(NFLTeam).filter(NFLTeam.team_abbr == team_abbr, NFLTeam.season == season).first()


@router.get("/players")
def get_players(
    season: int = Query(2024),
    position: Optional[str] = None,
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(NFLPlayer).filter(NFLPlayer.season == season)
    if position:
        q = q.filter(NFLPlayer.position == position)
    if team:
        q = q.filter(NFLPlayer.team == team)
    return q.all()


@router.get("/passing")
def get_passing(
    season: int = Query(2024),
    min_attempts: int = Query(100),
    db: Session = Depends(get_db),
):
    return (
        db.query(NFLPassingStats)
        .filter(NFLPassingStats.season == season, NFLPassingStats.attempts >= min_attempts)
        .all()
    )


@router.get("/rushing")
def get_rushing(
    season: int = Query(2024),
    min_carries: int = Query(50),
    db: Session = Depends(get_db),
):
    return (
        db.query(NFLRushingStats)
        .filter(NFLRushingStats.season == season, NFLRushingStats.carries >= min_carries)
        .all()
    )


@router.get("/receiving")
def get_receiving(
    season: int = Query(2024),
    min_targets: int = Query(30),
    position: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = (
        db.query(NFLReceivingStats)
        .filter(NFLReceivingStats.season == season, NFLReceivingStats.targets >= min_targets)
    )
    return q.all()
