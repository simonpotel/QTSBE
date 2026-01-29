from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
import os, sys, json, importlib.util
from dotenv import load_dotenv

load_dotenv()

from core.analysis import analyse
from routes.analyse import register_analyse_routes
from routes.analyse_custom import register_analyse_custom_routes
from routes.strategies import register_strategy_routes
from routes.get_tokens import register_get_tokens_routes
from routes.get_tokens_stats import register_get_tokens_stats_routes
from routes.health import register_health_routes

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

def load_config():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'api.json')
    with open(path, 'r') as f: return json.load(f)

def import_strategies(folder):
    strats = {}
    if not os.path.exists(folder): return strats
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                name = os.path.relpath(path, folder).replace(os.sep, '_').rsplit('.', 1)[0]
                try:
                    spec = importlib.util.spec_from_file_location(os.path.splitext(f)[0], path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    if all(hasattr(mod, a) for a in ['buy_signal', 'sell_signal', 'Indicators']):
                        strats[name] = {"buy_signal": mod.buy_signal, "sell_signal": mod.sell_signal, "Indicators": mod.Indicators}
                except Exception: pass
    return strats

def create_app():
    app = Flask(__name__)
    app.config['CACHE_TYPE'] = os.getenv('QTSBE_CACHE_TYPE')
    app.config['CACHE_DEFAULT_TIMEOUT'] = int(os.getenv('QTSBE_CACHE_DEFAULT_TIMEOUT'))
    Cache(app)
    
    origins = os.getenv('QTSBE_CORS_ORIGINS', '*').split(',')
    CORS(app, resources={r"/QTSBE/*": {"origins": origins}})

    strats = import_strategies("api/strategies")
    register_analyse_routes(app, strats, analyse)
    register_analyse_custom_routes(app, analyse)
    register_strategy_routes(app, strats)
    register_get_tokens_routes(app)
    register_get_tokens_stats_routes(app)
    register_health_routes(app)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=os.getenv('QTSBE_HOST'), port=int(os.getenv('QTSBE_PORT')), debug=os.getenv('QTSBE_DEBUG', 'false').lower() == 'true')
