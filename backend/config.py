import os
from dotenv import load_dotenv

load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sports.db")

# External API keys
CFBD_API_KEY = os.getenv("CFBD_API_KEY", "")  # College Football Data API (free)

# Data refresh settings
MLB_SEASON = int(os.getenv("MLB_SEASON", "2025"))
NFL_SEASON = int(os.getenv("NFL_SEASON", "2024"))
NCAA_FB_SEASON = int(os.getenv("NCAA_FB_SEASON", "2024"))
NCAA_BB_SEASON = os.getenv("NCAA_BB_SEASON", "2024-25")
