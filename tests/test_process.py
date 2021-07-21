import concurrent.futures
import json
from currency_xch_api.main import XchApi

def test_process_request(json_example1):
    """Test the correct reception of a json request
    """
    api_obj = XchApi()
    assert api_obj
    transaction = json.loads(api_obj.process_request(json_example1))
    assert transaction
    assert type(transaction) == dict
    assert transaction["from"]
    assert transaction["to"]
    assert transaction["qty"]
    assert transaction["total"]
    assert transaction["fee"]

def test_multiple_process_request(json_example1, json_example2, json_example3):
    """Test the correct reception of a json request
    """
    api_obj = XchApi()
    assert api_obj
    assert api_obj.currencies[0].qty_available == api_obj.currencies[1].qty_available == api_obj.currencies[5].qty_available == 1000
    request_jsons = [json_example1, json_example2, json_example3]
    res = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=22) as executor:
        futures = executor.map(api_obj.process_request, request_jsons)
        for future in futures:
            res.append(json.loads(future))
    assert res
    assert len(res) == 3
    assert type(res[0]) == dict
    assert [c != 1000 for c in (api_obj.currencies[0].qty_available, api_obj.currencies[1].qty_available, api_obj.currencies[5].qty_available)]