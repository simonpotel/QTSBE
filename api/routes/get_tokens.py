from flask import jsonify
from datetime import datetime
from loguru import logger
import os

def register_get_tokens_routes(app):
    @app.route('/QTSBE/get_tokens')
    def get_tokens():
        try:
            bank_path = "data/bank"
            tokens = {}
            
            for filename in os.listdir(bank_path):
                if filename.endswith('.csv'):
                    parts = filename[:-4].split('_')
                    if len(parts) >= 3:
                        exchange, pair, timeframe = parts[0], parts[1], parts[2]
                        tokens.setdefault(exchange, {}).setdefault(pair, []).append(timeframe)

            response_data = {
                "tokens": tokens,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info("Get tokens request successful")
            return jsonify(response_data)
            
        except Exception as e:
            error_msg = f"Error in get_tokens: {str(e)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 500 