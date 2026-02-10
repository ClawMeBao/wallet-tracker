import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def get_env(name: str, default: str | None = None, required: bool = False) -> str | None:
    val = os.getenv(name, default)
    if required and not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


@dataclass
class Settings:
    telegram_bot_token: str
    ankr_api_key: str
    sheet_id: str
    sheets_credentials_path: str
    log_level: str = "INFO"
    track_interval_minutes: int = 5
    prod_interval_minutes: int = 360
    state_path: str = "./data/state.json"


def load_settings() -> Settings:
    return Settings(
        telegram_bot_token=get_env("TELEGRAM_BOT_TOKEN", required=True),
        ankr_api_key=get_env("ANKR_API_KEY", required=True),
        sheet_id=get_env("SHEET_ID", required=True),
        sheets_credentials_path=get_env("SHEETS_CREDENTIALS_PATH", "./credentials.json"),
        log_level=get_env("LOG_LEVEL", "INFO"),
        track_interval_minutes=int(get_env("TRACK_INTERVAL_MINUTES", "5")),
        prod_interval_minutes=int(get_env("PROD_INTERVAL_MINUTES", "360")),
        state_path=get_env("STATE_PATH", "./data/state.json"),
    )
