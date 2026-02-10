import asyncio
import logging

from .config import load_settings
from .state import StateStore
from .tracker import Tracker
from .sheets import ensure_headers
from .bot import build_app


logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main():
    settings = load_settings()
    ensure_headers(settings.sheets_credentials_path, settings.sheet_id)

    state = StateStore(settings.state_path)
    state.set_interval(settings.track_interval_minutes)

    tracker = Tracker(settings.ankr_api_key, state, settings.sheet_id, settings.sheets_credentials_path)
    stop_event = asyncio.Event()

    async def run_tracker_loop():
        await tracker.loop_run(state.state.interval_minutes, stop_event)

    async def run_bot():
        app = build_app(settings.telegram_bot_token, state, tracker, tracker.run_once, stop_event)
        await app.initialize()
        await app.start()
        await app.updater.start_polling()
        await app.updater.idle()

    async def orchestrator():
        loop_task = asyncio.create_task(run_tracker_loop())
        bot_task = asyncio.create_task(run_bot())
        await asyncio.wait([loop_task, bot_task], return_when=asyncio.FIRST_COMPLETED)

    asyncio.run(orchestrator())


if __name__ == "__main__":
    main()
