from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.ncaa_bb import NCAABBTeam, NCAABBTeamStats

router = APIRouter()


@router.get("/teams")
def get_teams(
    season: str = Query("2024-25"),
    conference: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(NCAABBTeam).filter(NCAABBTeam.season == season)
    if conference:
        q = q.filter(NCAABBTeam.conference == conference)
    return q.all()


@router.get("/teams/{team_id}")
def get_team(team_id: str, season: str = Query("2024-25"), db: Session = Depends(get_db)):
    return db.query(NCAABBTeam).filter(NCAABBTeam.team_id == team_id, NCAABBTeam.season == season).first()


@router.get("/stats")
def get_team_stats(
    season: str = Query("2024-25"),
    conference: Optional[str] = None,
    sort_by: str = Query("net_efficiency"),
    db: Session = Depends(get_db),
):
    q = db.query(NCAABBTeamStats).filter(NCAABBTeamStats.season == season)
    results = q.all()
    results.sort(key=lambda x: getattr(x, sort_by, 0) or 0, reverse=True)
    return results
