import asyncio
from datetime import datetime
from typing import Dict, List

import pandas as pd

from .ankr_client import AnkrClient
from .pricing import fetch_prices_usd
from .sheets import append_rows
from .state import StateStore


class Tracker:
    def __init__(self, ankr_api_key: str, state: StateStore, sheet_id: str, creds_path: str):
        self.ankr = AnkrClient(ankr_api_key)
        self.state = state
        self.sheet_id = sheet_id
        self.creds_path = creds_path

    async def run_once(self) -> Dict:
        wallets = self.state.state.wallets
        if not wallets:
            return {"summary": {}, "rows": []}

        all_rows = []
        price_symbols = set()
        token_records = []

        for w in wallets:
            balances = await self.ankr.get_token_balances(w.chain, w.address)
            for b in balances:
                symbol = b.get("symbol") or b.get("tokenSymbol") or "?"
                amount = float(b.get("balance") or 0)
                token_records.append({
                    "chain": w.chain,
                    "address": w.address,
                    "token": symbol.lower(),
                    "amount": amount,
                })
                price_symbols.add(symbol.lower())

        prices = fetch_prices_usd(list(price_symbols))

        timestamp = datetime.utcnow().isoformat()
        for rec in token_records:
            usd = rec["amount"] * float(prices.get(rec["token"], 0))
            all_rows.append([
                timestamp,
                rec["chain"],
                rec["address"],
                rec["token"],
                rec["amount"],
                usd,
            ])

        if all_rows:
            append_rows(self.creds_path, self.sheet_id, all_rows)

        df = pd.DataFrame(all_rows, columns=["timestamp", "chain", "address", "token", "amount", "usd"])
        summary = {}
        if not df.empty:
            summary = (
                df.groupby("token")["usd"].sum().sort_values(ascending=False).to_dict()
            )

        return {"summary": summary, "rows": all_rows}

    async def loop_run(self, interval_minutes: int, stop_event: asyncio.Event):
        while not stop_event.is_set():
            try:
                await self.run_once()
            except Exception as e:
                print(f"[tracker] error: {e}")
            await asyncio.wait([stop_event.wait()], timeout=interval_minutes * 60)
