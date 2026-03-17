from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.ncaa_fb import NCAAFBPlayer, NCAAFBPassingStats, NCAAFBRushingStats, NCAAFBReceivingStats

router = APIRouter()


@router.get("/players")
def get_players(
    season: int = Query(2024),
    position: Optional[str] = None,
    conference: Optional[str] = None,
    team: Optional[str] = None,
    db: Session = Depends(get_db),
):
    q = db.query(NCAAFBPlayer).filter(NCAAFBPlayer.season == season)
    if position:
        q = q.filter(NCAAFBPlayer.position == position)
    if conference:
        q = q.filter(NCAAFBPlayer.conference == conference)
    if team:
        q = q.filter(NCAAFBPlayer.team == team)
    return [r.to_dict() for r in q.all()]


@router.get("/passing")
def get_passing(
    season: int = Query(2024),
    min_attempts: int = Query(50),
    db: Session = Depends(get_db),
):
    return [r.to_dict() for r in
        db.query(NCAAFBPassingStats)
        .filter(NCAAFBPassingStats.season == season, NCAAFBPassingStats.attempts >= min_attempts)
        .all()
    ]


@router.get("/rushing")
def get_rushing(
    season: int = Query(2024),
    min_carries: int = Query(30),
    db: Session = Depends(get_db),
):
    return [r.to_dict() for r in
        db.query(NCAAFBRushingStats)
        .filter(NCAAFBRushingStats.season == season, NCAAFBRushingStats.carries >= min_carries)
        .all()
    ]


@router.get("/receiving")
def get_receiving(
    season: int = Query(2024),
    min_targets: int = Query(20),
    db: Session = Depends(get_db),
):
    return [r.to_dict() for r in
        db.query(NCAAFBReceivingStats)
        .filter(NCAAFBReceivingStats.season == season, NCAAFBReceivingStats.targets >= min_targets)
        .all()
    ]
