from typing import List
from currency_xch_api.exchange import Exchange
from dataclasses import dataclass

@dataclass
class Currency:
    name: str
    qty_available: float
    exchange_rates: List[Exchange]
    
    def add_exchange_rate(self, name_to: str, rate: float):
        ex = Exchange(self.name, name_to, rate)
        self.exchange_rates.append(ex)
        return ex