import json
from currency_xch_api.main import XchApi

def test_get_json(json_example):
    """Test the correct reception of a json request
    """
    api_obj = XchApi()
    assert api_obj
    quote = api_obj._parse_json_to_quote(json_example)
    assert quote
    assert type(quote) == dict
    assert quote["from"]
    assert quote["to"]
    assert quote["qty"]

def test_get_currencies(json_example):
    """Test the correct creation of default currencies
    """
    api_obj = XchApi()
    assert api_obj.currencies
    assert api_obj.currencies[0].name == "EUR"
    assert api_obj.currencies[1].name == "USD"
    assert api_obj.currencies[0].exchange_rates
    assert api_obj.currencies[1].exchange_rates
    assert api_obj.currencies[1].exchange_rates[0].rate == round(1 / api_obj.currencies[0].exchange_rates[0].rate, 4)
    assert len(api_obj.currencies) == 8
    assert len(api_obj.currencies[0].exchange_rates) == 7