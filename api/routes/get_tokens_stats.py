from flask import jsonify
from datetime import datetime
from loguru import logger
import os
import pandas as pd

def register_get_tokens_stats_routes(app):
    @app.route('/QTSBE/get_tokens_stats')
    def get_tokens_stats():
        try:
            bank_path = "data/bank"
            tokens = {}
            
            for filename in os.listdir(bank_path):
                if filename.endswith('.csv'):
                    parts = filename[:-4].split('_')
                    if len(parts) >= 3:
                        exchange = parts[0]
                        pair = parts[1]
                        timeframe = parts[2]
                        
                        try:
                            filepath = os.path.join(bank_path, filename)
                            df = pd.read_csv(filepath, parse_dates=['timestamp'], infer_datetime_format=True)
                            df.dropna(subset=['timestamp'], inplace=True)
                            
                            if not df.empty:
                                token_info = {
                                    'timeframes': [timeframe],
                                    'first_date': df['timestamp'].min().strftime("%Y-%m-%d %H:%M:%S"),
                                    'last_date': df['timestamp'].max().strftime("%Y-%m-%d %H:%M:%S"),
                                    'last_price': float(df.iloc[-1]['close']),
                                    'volume_24h': float(df.iloc[-1]['volume']),
                                    'price_change_24h': float((df.iloc[-1]['close'] - df.iloc[-2]['close']) / df.iloc[-2]['close'] * 100) if len(df) > 1 else 0.0
                                }
                                
                                if exchange not in tokens:
                                    tokens[exchange] = {}
                                if pair not in tokens[exchange]:
                                    tokens[exchange][pair] = token_info
                                else:
                                    tokens[exchange][pair]['timeframes'].append(timeframe)
                        
                        except Exception as e:
                            logger.error(f"Error processing file {filename}: {str(e)}")
                            continue

            response_data = {
                "tokens": tokens,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info("Get tokens stats request successful")
            return jsonify(response_data)
            
        except Exception as e:
            error_msg = f"Error in get_tokens_stats: {str(e)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 500 