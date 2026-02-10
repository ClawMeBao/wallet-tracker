import logging

from .config import load_settings
from .state import StateStore
from .tracker import Tracker
from .bot import build_app


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    settings = load_settings()

    state = StateStore(settings.state_path)
    state.set_interval(settings.track_interval_minutes)

    tracker = Tracker(settings.ankr_api_key, state, settings.output_csv_path)

    app = build_app(settings.telegram_bot_token, state, settings.output_csv_path, tracker.run_once)
    # run_polling is blocking and manages its own loop
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
