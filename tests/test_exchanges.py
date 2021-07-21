import concurrent.futures
from currency_xch_api.main import XchApi

def test_calculate_correct():
    """Test the correct calculation of a exchange
    """
    api_obj = XchApi()
    assert api_obj
    quote = {
        "from": "USD",
        "to": "NZD",
        "qty": 2
    }
    res = api_obj._calculate_exchange_operation(quote)
    assert res
    assert res["result"]
    assert res["fee"]
    assert type(res["result"]) == float
    assert type(res["fee"]) == float

def test_update_currencies_correct():
    """Test the correct calculation of a exchange
    """
    api_obj = XchApi()
    assert api_obj
    quote = {
        "from": "USD",
        "to": "NZD",
        "qty": 2
    }
    charges = {
        "result": 5,
        "fee": 0.1
    }
    api_obj._update_currencies(quote, charges["result"])
    assert api_obj.currencies[1].qty_available == 1002
    assert api_obj.currencies[7].qty_available == 995

    
def test_update_currencies_concurrent():
    """Test the correct calculation of concurrent exchanges
    """
    api_obj = XchApi()
    assert api_obj
    quote = {
        "from": "USD",
        "to": "NZD",
        "qty": 20
    }
    charges = {
        "result": 50,
        "fee": 0.1
    }
    quote2 = {
        "from": "NZD",
        "to": "USD",
        "qty": 30
    }
    charges2 = {
        "result": 12,
        "fee": 0.1
    }
    with concurrent.futures.ProcessPoolExecutor(max_workers=22) as executor:
        futures = [executor.submit(api_obj._update_currencies(quote, charges["result"]), i) for i in range(0,10)]
        futures2 = [executor.submit(api_obj._update_currencies(quote2, charges2["result"]), i) for i in range(0,10)]
    # USD = 1000 + (20 * 10) - (12 * 10) = 1080
    assert api_obj.currencies[1].qty_available == 1080
    # NZD = 1000 - (50 * 10) + (30 * 10) = 800
    assert api_obj.currencies[7].qty_available == 800

def test_add_fees():
    api_obj = XchApi()
    assert api_obj
    quote = {
        "from": "USD",
        "to": "NZD",
        "qty": 20
    }
    charges = {
        "result": 49,
        "fee": 1
    }
    api_obj._add_fee(quote, charges["fee"])
    api_obj._add_fee(quote, charges["fee"])
    api_obj._add_fee(quote, charges["fee"])
    assert api_obj.fees_charged
    assert api_obj.fees_charged[0].value == 1
    assert sum(f.value for f in api_obj.fees_charged) == 3
