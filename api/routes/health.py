from flask import jsonify
from loguru import logger
import ccxt

def register_health_routes(app):
    @app.route('/QTSBE/health')
    def health_check():
        try:
            exchange = ccxt.binance()
            
            server_time = exchange.fetch_time()
            
            if server_time:
                logger.info("Health check successful - Binance connection working")
                return jsonify({
                    "status": "healthy",
                    "message": "QTSBE service is running and Binance connection is working",
                    "binance_status": "connected",
                    "server_time": server_time
                }), 200
            else:
                logger.warning("Health check warning - Binance response incomplete")
                return jsonify({
                    "status": "warning", 
                    "message": "Service running but Binance response incomplete",
                    "binance_status": "partial"
                }), 200
                
        except Exception as e:
            logger.error(f"Health check failed - Binance connection error: {e}")
            return jsonify({
                "status": "unhealthy",
                "message": "Service running but Binance connection failed",
                "binance_status": "disconnected",
                "error": str(e)
            }), 503 