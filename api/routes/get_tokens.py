from flask import jsonify
from datetime import datetime
from core.data_utils import list_keys

def register_get_tokens_routes(app):
    @app.route('/QTSBE/get_tokens')
    def get_tokens():
        tokens = {}
        for key in list_keys():
            parts = key.split('_')
            if len(parts) >= 3:
                tokens.setdefault(parts[0], {}).setdefault(parts[1], []).append(parts[2])
        return jsonify({"tokens": tokens, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})