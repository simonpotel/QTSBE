import json

def test_health(client):
    res = client.get('/QTSBE/health')
    assert res.status_code == 200
    assert res.json['status'] == 'healthy'

def test_get_tokens(client):
    res = client.get('/QTSBE/get_tokens')
    assert res.status_code == 200
    assert 'tokens' in res.json

def test_get_tokens_stats(client):
    res = client.get('/QTSBE/get_tokens_stats')
    assert res.status_code == 200
    assert 'tokens' in res.json

def test_get_strategies(client):
    res = client.get('/QTSBE/get_strategies')
    assert res.status_code == 200
    assert 'strategies' in res.json

def test_analyse(client):
    params = {
        'pair': 'Binance_BTCUSDC_1d',
        'strategy': 'default',
        'position_type': 'long'
    }
    res = client.get('/QTSBE/analyse', query_string=params)
    assert res.status_code == 200
    assert 'stats' in res.json

def test_analyse_custom(client):
    strategy_code = """
def Indicators(data):
    class I:
        def __init__(self, d): self.indicators = {}
    return I(data)
def buy_signal(positions, data, i, indicators): return 1 if i > 0 else 0, data[i][4]
def sell_signal(position, data, i, indicators): return 1 if i > 5 else 0, data[i][4]
"""
    params = {
        'pair': 'Binance_BTCUSDC_1d',
        'position_type': 'long'
    }
    res = client.post('/QTSBE/analyse_custom', 
                     query_string=params,
                     data=json.dumps({'strategy_code': strategy_code}),
                     content_type='application/json')
    assert res.status_code == 200
    assert 'stats' in res.json
