from currency_xch_api.currency import Currency
from currency_xch_api.exchange import Exchange
from currency_xch_api.fee import Fee
import json
import random
import threading
from typing import List

FEE_PERCENTAGE = 2.0
lock = threading.Lock()

class XchApi:
    currencies: List[Currency]
    fees_charged: List[Fee]

    def __init__(self):
        self.currencies = []
        self.fees_charged = []
        self._set_default_currencies()

    def _set_default_currencies(self):        
        EUR = Currency("EUR", 1000, [])
        self.set_currency(EUR)
        USD = Currency("USD", 1000, [])
        self.set_currency(USD)
        JPY = Currency("JPY", 1000, [])
        self.set_currency(JPY)
        GBP = Currency("GBP", 1000, [])
        self.set_currency(GBP)
        CHF = Currency("CHF", 1000, [])
        self.set_currency(CHF)
        AUD = Currency("AUD", 1000, [])
        self.set_currency(AUD)
        CAD = Currency("CAD", 1000, [])
        self.set_currency(CAD)
        NZD = Currency("NZD", 1000, [])
        self.set_currency(NZD)
    
    def set_currency(self, currency: Currency):
        for c in self.currencies:
            rate = random.uniform(0.01, 10)
            c.add_exchange_rate(currency.name, round(rate, 4))
            currency.add_exchange_rate(c.name, round(1/rate, 4))
        self.currencies.append(currency)

    def process_request(self,  json_str : json) -> json:
        quote = self._parse_json_to_quote(json_str)
        charges = self._calculate_exchange_operation(quote)
        self._update_currencies(quote, charges["result"])
        self._add_fee(quote, charges["fee"])
        quote.update({
            "total": sum(charges.values()),
            "fee": charges["fee"]
        })
        return json.dumps(quote)

    def _parse_json_to_quote(self, json_str : json):
        return json.loads(json_str)        
        
    def _calculate_exchange_operation(self, quote : dict) -> dict:
        exchange_rate = 0.0
        for c in self.currencies:
            for e in c.exchange_rates:
                if e.name_from == quote["from"] and e.name_to == quote["to"]:
                    exchange_rate = e.rate
        if not exchange_rate:
            raise Exception("Exchange rate not found!")
        exchange_fee = quote["qty"] * (FEE_PERCENTAGE / 100) * exchange_rate
        exchange_result = quote["qty"] * (1 - FEE_PERCENTAGE / 100) * exchange_rate
        return {
            "fee": exchange_fee,
            "result": exchange_result
        }

    def _update_currencies(self, quote : dict, charge : float):
        operation_available = False
        for c in self.currencies:
            if c.name == quote["to"]:
                lock.acquire()
                if c.qty_available >= charge:
                    c.qty_available -= charge
                    operation_available = True
                lock.release()
        if not operation_available:
            raise Exception("There are not enough founds to fullfill the operation")
        for c in self.currencies:
            if c.name == quote["from"]:
                lock.acquire()
                c.qty_available += quote["qty"]
                lock.release()

    def _add_fee(self, quote : dict, charge : float):
        fee = Fee(quote["from"], quote["to"], charge)
        self.fees_charged.append(fee)
