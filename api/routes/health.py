from flask import jsonify
import ccxt

def register_health_routes(app):
    @app.route('/QTSBE/health')
    def health_check():
        try:
            exchange = ccxt.binance()
            server_time = exchange.fetch_time()
            if server_time:
                return jsonify({"status": "healthy", "binance": "connected", "time": server_time}), 200
            return jsonify({"status": "warning", "binance": "partial"}), 200
        except Exception as e:
            return jsonify({"status": "unhealthy", "binance": "error", "error": str(e)}), 503