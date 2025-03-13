import pytest
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:5002/QTSBE"

@pytest.fixture
def api_client():
    return requests.Session()

def test_analyse_endpoint_success(api_client):
    params = {
        "pair": "Binance_ETHUSDT_1d",
        "strategy": "rsi_example",
        "details": "True",
        "position_type": "long"
    }
    response = api_client.get(f"{BASE_URL}/analyse", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "pair" in data
    assert "strategy" in data
    assert "data" in data
    assert "result" in data
    assert "stats" in data
    assert "position_type" in data
    assert data["position_type"] == "long"

def test_analyse_endpoint_missing_params(api_client):
    response = api_client.get(f"{BASE_URL}/analyse")
    assert response.status_code == 400
    assert "error" in response.json()

def test_analyse_endpoint_invalid_pair(api_client):
    params = {
        "pair": "INVALID_PAIR",
        "strategy": "rsi_example"
    }
    response = api_client.get(f"{BASE_URL}/analyse", params=params)
    assert response.status_code == 404

def test_analyse_endpoint_with_timestamps(api_client):
    end_ts = datetime.now()
    start_ts = end_ts - timedelta(days=30)
    params = {
        "pair": "Binance_ETHUSDT_1d",
        "strategy": "rsi_example",
        "start_ts": start_ts.strftime("%Y-%m-%d %H:%M:%S"),
        "end_ts": end_ts.strftime("%Y-%m-%d %H:%M:%S"),
        "position_type": "long"
    }
    response = api_client.get(f"{BASE_URL}/analyse", params=params)
    assert response.status_code == 200

def test_analyse_endpoint_short_position(api_client):
    params = {
        "pair": "Binance_ETHUSDT_1d",
        "strategy": "rsi_example",
        "details": "True",
        "position_type": "short"
    }
    response = api_client.get(f"{BASE_URL}/analyse", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "position_type" in data
    assert data["position_type"] == "short"

def test_analyse_endpoint_invalid_position_type(api_client):
    params = {
        "pair": "Binance_ETHUSDT_1d",
        "strategy": "rsi_example",
        "position_type": "invalid"
    }
    response = api_client.get(f"{BASE_URL}/analyse", params=params)
    assert response.status_code == 400
    assert "error" in response.json()
    assert "position_type must be either 'long' or 'short'" in response.json()["error"]

def test_analyse_custom_endpoint_success(api_client):
    params = {
        "pair": "Binance_ETHUSDT_1d",
        "details": "True",
        "position_type": "long"
    }
    strategy_code = """
import numpy as np

def get_RSI(prices, window=14):
    deltas = np.diff(prices)
    seed = deltas[:window+1]
    up = seed[seed >= 0].sum() / window
    down = -seed[seed < 0].sum() / window
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:window] = 100. - 100. / (1. + rs)
    return rsi

class Indicators:
    def __init__(self, data):
        self.data = data
        self.indicators = self.calculate_indicators()

    def calculate_indicators(self):
        data_open = [row[1] for row in self.data]
        indicators = {"RSI": get_RSI(data_open)}
        return {k: list(v) for k, v in indicators.items()}

def buy_signal(open_position, data, index_check, indicators, current_price=None):
    if current_price is not None:
        data[index_check][4] = current_price
    if indicators["RSI"][index_check] is None:
        return -2, None
    if indicators["RSI"][index_check] < 40:
        return 1, data[index_check][4]
    return 0, None

def sell_signal(open_position, data, index_check, indicators, current_price=None):
    if current_price is not None:
        data[index_check][4] = current_price
    if indicators["RSI"][index_check] is None:
        return -1, None
    if indicators["RSI"][index_check] > 60:
        return 1, data[index_check][4]
    return 0, None
"""
    response = api_client.post(f"{BASE_URL}/analyse_custom", params=params, json={"strategy_code": strategy_code})
    assert response.status_code == 200
    data = response.json()
    assert "pair" in data
    assert "strategy" in data
    assert "data" in data
    assert "result" in data
    assert "stats" in data
    assert "position_type" in data
    assert data["position_type"] == "long"

def test_analyse_custom_endpoint_missing_params(api_client):
    headers = {'Content-Type': 'application/json'}
    response = api_client.post(f"{BASE_URL}/analyse_custom", headers=headers, json={})
    assert response.status_code == 400
    assert "error" in response.json()

def test_analyse_custom_endpoint_invalid_code(api_client):
    params = {
        "pair": "Binance_ETHUSDT_1d"
    }
    strategy_code = "invalid python code"
    response = api_client.post(f"{BASE_URL}/analyse_custom", params=params, json={"strategy_code": strategy_code})
    assert response.status_code == 400
    assert "error" in response.json()

def test_get_tokens_endpoint(api_client):
    response = api_client.get(f"{BASE_URL}/get_tokens")
    assert response.status_code == 200
    data = response.json()
    assert "tokens" in data
    assert "timestamp" in data
    assert isinstance(data["tokens"], dict)

def test_get_strategies_endpoint(api_client):
    response = api_client.get(f"{BASE_URL}/get_strategies")
    assert response.status_code == 200
    data = response.json()
    assert "strategies" in data
    assert "timestamp" in data
    assert isinstance(data["strategies"], list)

def test_get_tokens_stats_endpoint(api_client):
    response = api_client.get(f"{BASE_URL}/get_tokens_stats")
    assert response.status_code == 200
    data = response.json()
    assert "tokens" in data
    assert "timestamp" in data
    assert isinstance(data["tokens"], dict)
    
    for exchange in data["tokens"].values():
        for token_info in exchange.values():
            assert "timeframes" in token_info
            assert "first_date" in token_info
            assert "last_date" in token_info
            assert "last_price" in token_info
            assert "volume_24h" in token_info
            assert "price_change_24h" in token_info
            assert "last_modified" in token_info 