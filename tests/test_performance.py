import time
import pytest

def run_performance_test(client, pair):
    params = {
        'pair': pair,
        'strategy': 'default',
        'position_type': 'long',
        'details': 'True'
    }
    start = time.time()
    res = client.get('/QTSBE/analyse', query_string=params)
    duration = time.time() - start
    
    if res.status_code == 200:
        bar_count = len(res.json.get('data', []))
        print(f"\nPerformance for {pair}: {duration:.4f}s ({bar_count} bars) -> { (duration/bar_count*1000) if bar_count > 0 else 0 :.4f}ms/bar")
    else:
        print(f"\nFailed to test {pair}: {res.status_code} - {res.json.get('error')}")
    
    assert res.status_code == 200

def test_analyze_performance_1d(client):
    run_performance_test(client, 'Binance_BTCUSDC_1d')

def test_analyze_performance_1w(client):
    run_performance_test(client, 'Binance_BTCUSDC_1w')

def test_analyze_performance_1s(client):
    run_performance_test(client, 'Binance_BTCUSDC_1s')
