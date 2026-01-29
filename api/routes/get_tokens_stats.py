from flask import jsonify
from datetime import datetime
from loguru import logger
import os
import h5py
import pandas as pd

def register_get_tokens_stats_routes(app):
    @app.route('/QTSBE/get_tokens_stats')
    def get_tokens_stats():
        try:
            tokens = {}
            h5_path = "data/bank/qtsbe_data.h5"
            
            if os.path.exists(h5_path):
                with h5py.File(h5_path, 'r') as f:
                    for key in f.keys():
                        data = f[key][:]
                        if len(data) == 0: continue
                        
                        parts = key.split('_')
                        if len(parts) < 3: continue
                        ex, p, tf = parts[0], parts[1], parts[2]
                        
                        latest = data[-1]
                        prev_close = data[-2][4] if len(data) > 1 else latest[4]
                        
                        stats = {
                            'timeframes': [tf],
                            'first_date': datetime.fromtimestamp(data[0][0]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                            'last_date': datetime.fromtimestamp(latest[0]/1000).strftime("%Y-%m-%d %H:%M:%S"),
                            'last_price': float(latest[4]),
                            'volume_24h': float(latest[5]),
                            'price_change_24h': float((latest[4] - prev_close) / prev_close * 100) if prev_close else 0.0,
                            'last_modified': datetime.fromtimestamp(os.path.getmtime(h5_path)).strftime("%Y-%m-%d %H:%M:%S")
                        }
                        
                        if ex not in tokens: tokens[ex] = {}
                        if p not in tokens[ex]: tokens[ex][p] = stats
                        else: tokens[ex][p]['timeframes'].append(tf)

            return jsonify({"tokens": tokens, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except Exception as e:
            logger.error(f"Stats error: {e}")
            return jsonify({"error": str(e)}), 500