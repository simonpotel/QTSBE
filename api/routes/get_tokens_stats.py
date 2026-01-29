from flask import jsonify
from datetime import datetime
import os
from core.data_utils import list_keys, get_data

def register_get_tokens_stats_routes(app):
    @app.route('/QTSBE/get_tokens_stats')
    def get_tokens_stats():
        tokens = {}
        h5_path = "data/bank/qtsbe_data.h5"
        for key in list_keys():
            data = get_data(key, limit=2)
            if not data: continue
            
            parts = key.split('_')
            if len(parts) < 3: continue
            ex, p, tf = parts[0], parts[1], parts[2]
            
            latest = data[-1]
            prev_close = data[-2][4] if len(data) > 1 else latest[4]
            
            stats = {
                'timeframes': [tf],
                'first_date': data[0][0],
                'last_date': latest[0],
                'last_price': float(latest[4]),
                'volume_24h': float(latest[5]),
                'price_change_24h': float((latest[4] - prev_close) / prev_close * 100) if prev_close else 0.0,
                'last_modified': datetime.fromtimestamp(os.path.getmtime(h5_path)).strftime("%Y-%m-%d %H:%M:%S")
            }
            
            if ex not in tokens: tokens[ex] = {}
            if p not in tokens[ex]: tokens[ex][p] = stats
            else: tokens[ex][p]['timeframes'].append(tf)

        return jsonify({"tokens": tokens, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})