import asyncio
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
    stop_event = asyncio.Event()

    async def run_tracker_loop():
        await tracker.loop_run(state.state.interval_minutes, stop_event)

    async def orchestrator():
        app = build_app(settings.telegram_bot_token, state, settings.output_csv_path, tracker.run_once, stop_event)
        tracker_task = asyncio.create_task(run_tracker_loop())
        bot_task = asyncio.create_task(app.run_polling())
        done, pending = await asyncio.wait({tracker_task, bot_task}, return_when=asyncio.FIRST_EXCEPTION)
        for task in pending:
            task.cancel()

    asyncio.run(orchestrator())


if __name__ == "__main__":
    main()
