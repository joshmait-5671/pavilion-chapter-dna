import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_BOT_NAME = os.environ.get("SLACK_BOT_NAME", "Ben from Forge")
HIVE_BRIGHT_API_KEY = os.environ.get("HIVE_BRIGHT_API_KEY", "")
HIVE_BRIGHT_BASE_URL = os.environ.get("HIVE_BRIGHT_BASE_URL", "https://api.hivebrite.com/v1")
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
KYLER_DRIVE_FOLDER_ID = os.environ.get("KYLER_DRIVE_FOLDER_ID", "")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "forge.db")

FORGE_MODEL = "claude-opus-4-6"
POD_SIZE = 6
FORGE_LEADER_THRESHOLD = 0.12  # Top 12% of cohort
