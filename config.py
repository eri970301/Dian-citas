import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

BASE_URL = os.getenv("BASE_URL")

CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "300"))

HEADLESS = os.getenv("HEADLESS", "True").lower() == "true"

LOG_FOLDER = "logs"

SCREENSHOT_FOLDER = "screenshots"

STATE_FILE = "state.json"