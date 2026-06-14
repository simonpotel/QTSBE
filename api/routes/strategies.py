from flask import jsonify
from datetime import datetime

def register_strategy_routes(app, strategies):
    @app.route('/QTSBE/get_strategies')
    def get_strategies():
        try:
            return jsonify({"strategies": list(strategies.keys()), "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/QTSBE/get_strategy_code')
    def get_strategy_code():
        import os
        from flask import request
        name = request.args.get('name')
        if not name:
            return jsonify({"error": "Missing strategy name"}), 400
        
        # Security: prevent directory traversal
        if '..' in name or '/' in name or '\\' in name:
            return jsonify({"error": "Invalid strategy name"}), 400
            
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'strategies', f"{name}.py")
        if not os.path.exists(file_path):
            return jsonify({"error": "Strategy not found"}), 404
            
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            return jsonify({"code": code})
        except Exception as e:
            return jsonify({"error": str(e)}), 500