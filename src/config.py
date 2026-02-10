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
    log_level: str = "INFO"
    track_interval_minutes: int = 5
    prod_interval_minutes: int = 360
    state_path: str = "./data/state.json"
    output_csv_path: str = "./data/balances.csv"


def load_settings() -> Settings:
    return Settings(
        telegram_bot_token=get_env("TELEGRAM_BOT_TOKEN", required=True),
        ankr_api_key=get_env("ANKR_API_KEY", required=True),
        log_level=get_env("LOG_LEVEL", "INFO"),
        track_interval_minutes=int(get_env("TRACK_INTERVAL_MINUTES", "5")),
        prod_interval_minutes=int(get_env("PROD_INTERVAL_MINUTES", "360")),
        state_path=get_env("STATE_PATH", "./data/state.json"),
        output_csv_path=get_env("OUTPUT_CSV_PATH", "./data/balances.csv"),
    )
