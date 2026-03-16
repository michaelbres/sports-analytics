from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import mlb, nfl, ncaa_fb, ncaa_bb


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Sports Analytics API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API routes
app.include_router(mlb.router, prefix="/api/mlb", tags=["MLB"])
app.include_router(nfl.router, prefix="/api/nfl", tags=["NFL"])
app.include_router(ncaa_fb.router, prefix="/api/ncaa-fb", tags=["NCAA Football"])
app.include_router(ncaa_bb.router, prefix="/api/ncaa-bb", tags=["NCAA Basketball"])


@app.get("/api/health")
def health():
    return {"status": "ok", "sports": ["mlb", "nfl", "ncaa_fb", "ncaa_bb"]}


# Serve frontend — must be last
app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
