"""
Admin router — trigger data pipelines server-side.
Protected by ADMIN_SECRET env var.
"""
import os
import threading
from fastapi import APIRouter, HTTPException, Header
from typing import Optional

router = APIRouter()

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "")

pipeline_status: dict[str, str] = {}


def _require_auth(x_admin_secret: Optional[str]):
    if not ADMIN_SECRET:
        raise HTTPException(status_code=500, detail="ADMIN_SECRET not configured on server")
    if x_admin_secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")


def _run_in_thread(name: str, fn):
    pipeline_status[name] = "running"
    def target():
        try:
            fn()
            pipeline_status[name] = "done"
        except Exception as e:
            pipeline_status[name] = f"error: {e}"
    threading.Thread(target=target, daemon=True).start()


@router.get("/status")
def get_status(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    return pipeline_status


@router.post("/run/mlb")
def run_mlb(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    from pipelines.mlb_pipeline import run
    _run_in_thread("mlb", run)
    return {"status": "started", "pipeline": "mlb"}


@router.post("/run/nfl")
def run_nfl(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    from pipelines.nfl_pipeline import run
    _run_in_thread("nfl", run)
    return {"status": "started", "pipeline": "nfl"}


@router.post("/run/ncaa-fb")
def run_ncaa_fb(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    from pipelines.ncaa_fb_pipeline import run
    _run_in_thread("ncaa_fb", run)
    return {"status": "started", "pipeline": "ncaa_fb"}


@router.post("/run/ncaa-bb")
def run_ncaa_bb(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    from pipelines.ncaa_bb_pipeline import run
    _run_in_thread("ncaa_bb", run)
    return {"status": "started", "pipeline": "ncaa_bb"}


@router.post("/run/all")
def run_all(x_admin_secret: Optional[str] = Header(None)):
    _require_auth(x_admin_secret)
    from pipelines.mlb_pipeline import run as mlb
    from pipelines.nfl_pipeline import run as nfl
    from pipelines.ncaa_fb_pipeline import run as ncaa_fb
    from pipelines.ncaa_bb_pipeline import run as ncaa_bb

    def run_all_pipelines():
        mlb(); nfl(); ncaa_fb(); ncaa_bb()

    _run_in_thread("all", run_all_pipelines)
    return {"status": "started", "pipeline": "all"}
