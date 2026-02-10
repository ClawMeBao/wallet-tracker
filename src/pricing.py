import requests
from typing import Dict, List

COINGECKO_SIMPLE_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_prices_usd(symbols: List[str]) -> Dict[str, float]:
    if not symbols:
        return {}
    try:
        ids = ",".join(symbols)
        resp = requests.get(COINGECKO_SIMPLE_URL, params={"ids": ids, "vs_currencies": "usd"}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {k: v.get("usd", 0) for k, v in data.items()}
    except Exception:
        return {}
