from flask import jsonify
from datetime import datetime

def register_strategy_routes(app, strategies):
    @app.route('/QTSBE/get_strategies')
    def get_strategies():
        try:
            return jsonify({"strategies": list(strategies.keys()), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except Exception as e:
            return jsonify({"error": str(e)}), 500