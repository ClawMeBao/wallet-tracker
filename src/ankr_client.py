from typing import List, Dict
from ankr import AnkrWeb3


class AnkrClient:
    def __init__(self, api_key: str):
        self.web3 = AnkrWeb3("https://rpc.ankr.com/multichain/" + api_key)

    async def get_token_balances(self, chain: str, address: str) -> List[Dict]:
        # Using AnkrWeb3 method: tokenBalance
        # docs: https://www.ankr.com/docs/advanced-api/python-sdk/
        return await self.web3.token.get_token_balance(chain, address)

    async def get_token_prices(self, symbols: List[str]) -> Dict[str, float]:
        # Ankr python SDK may not expose prices directly; fallback later if needed
        # Placeholder: return empty; pricing will be resolved in pricing.py
        return {}
