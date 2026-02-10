import httpx
from typing import List, Dict


class AnkrClient:
    def __init__(self, api_key: str):
        self.endpoint = f"https://rpc.ankr.com/multichain/{api_key}"

    async def get_token_balances(self, chain: str, address: str) -> List[Dict]:
        payload = {
            "jsonrpc": "2.0",
            "method": "ankr_getAccountBalance",
            "params": {"blockchain": chain, "address": address},
            "id": 1,
        }
        async with httpx.AsyncClient(timeout=15) as client:
            resp = await client.post(self.endpoint, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data.get("result", {}).get("tokens", [])

    async def get_token_prices(self, symbols: List[str]) -> Dict[str, float]:
        # Not used; pricing handled via external provider
        return {}
