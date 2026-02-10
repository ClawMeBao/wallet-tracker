import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List


@dataclass
class Wallet:
    chain: str
    address: str


@dataclass
class TrackerState:
    wallets: List[Wallet]
    interval_minutes: int


class StateStore:
    def __init__(self, path: str):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._state = TrackerState(wallets=[], interval_minutes=5)
        self.load()

    @property
    def state(self) -> TrackerState:
        return self._state

    def load(self):
        if not self.path.exists():
            return
        data = json.loads(self.path.read_text())
        self._state = TrackerState(
            wallets=[Wallet(**w) for w in data.get("wallets", [])],
            interval_minutes=data.get("interval_minutes", 5),
        )

    def save(self):
        data = asdict(self._state)
        # dataclasses to dict
        data["wallets"] = [asdict(w) for w in self._state.wallets]
        self.path.write_text(json.dumps(data, indent=2))

    def add_wallet(self, chain: str, address: str):
        if any(w.address.lower() == address.lower() for w in self._state.wallets):
            return False
        self._state.wallets.append(Wallet(chain=chain, address=address))
        self.save()
        return True

    def remove_wallet(self, address: str):
        before = len(self._state.wallets)
        self._state.wallets = [w for w in self._state.wallets if w.address.lower() != address.lower()]
        if len(self._state.wallets) != before:
            self.save()
            return True
        return False

    def set_interval(self, minutes: int):
        self._state.interval_minutes = minutes
        self.save()
