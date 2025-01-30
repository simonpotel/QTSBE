from flask import jsonify
from datetime import datetime
from loguru import logger

def register_strategy_routes(app, strategies):
    @app.route('/QTSBE/get_strategies')
    def get_strategies():
        try:
            response_data = {
                "strategies": list(strategies.keys()),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            logger.info("Get strategies request successful")
            return jsonify(response_data)
            
        except Exception as e:
            error_msg = f"Error in get_strategies: {str(e)}"
            logger.error(error_msg)
            return jsonify({"error": error_msg}), 500 