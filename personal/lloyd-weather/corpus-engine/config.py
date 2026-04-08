"""Paths, constants, and dimension definitions for the corpus engine."""
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths ──────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent
AUTH_DIR = ROOT / "auth"
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CORPUS_DIR = DATA_DIR / "corpus"
ANALYSIS_DIR = DATA_DIR / "analysis"
OUTPUT_DIR = ROOT / "output"

# ── Gmail ──────────────────────────────────────────────────────────────
GMAIL_SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
LLOYD_EMAIL = "lloydm5678@icloud.com"
CLIENT_SECRETS = AUTH_DIR / "client_secrets.json"
TOKEN_PATH = AUTH_DIR / "token.json"

# ── WhatsApp ───────────────────────────────────────────────────────────
WHATSAPP_CHAT_FILE = Path("/Users/joshmait/Desktop/wash-u-noobs-full-chat.txt")
LLOYD_NAMES = {"Lloyd", "Lloyd Mallah", "Lloyd M"}

# ── Weather keywords for filtering ─────────────────────────────────────
WEATHER_KEYWORDS = {
    "weather", "forecast", "snow", "rain", "storm", "temperature", "temp",
    "degrees", "wind", "humidity", "pressure", "precip", "precipitation",
    "nor'easter", "noreaster", "blizzard", "hurricane", "tornado", "hail",
    "thunder", "lightning", "ice", "sleet", "freezing", "frost", "fog",
    "cold front", "warm front", "low pressure", "high pressure",
    "gfs", "euro", "ecmwf", "nam", "hrrr", "model", "models",
    "accumulation", "inches", "snowfall", "rainfall", "flooding",
    "advisory", "warning", "watch", "nws", "national weather",
    "ski", "beach", "outdoor", "cancel", "delay", "school closing",
}

# ── Model name patterns for tagging ────────────────────────────────────
MODEL_PATTERNS = {
    "GFS": r"\bgfs\b",
    "ECMWF": r"\b(ecmwf|euro|european\s+model)\b",
    "NAM": r"\bnam\b",
    "HRRR": r"\bhrrr\b",
    "Ensemble": r"\b(ensemble|blend|nbm|grand\s+ensemble)\b",
}

# ── Weather type classification keywords ───────────────────────────────
WEATHER_TYPES = {
    "winter": {"snow", "ice", "sleet", "freezing", "blizzard", "nor'easter",
               "noreaster", "frost", "cold", "winter", "accumulation"},
    "severe": {"tornado", "hail", "supercell", "severe", "thunder",
               "lightning", "damaging wind"},
    "tropical": {"hurricane", "tropical", "storm surge", "category"},
    "daily": {"temperature", "rain", "sunny", "cloudy", "wind", "humidity",
              "fog", "forecast"},
}

# ── Claude ─────────────────────────────────────────────────────────────
CLAUDE_MODEL = "claude-sonnet-4-20250514"
BATCH_SIZE = 10
