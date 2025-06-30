from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_caching import Cache
from loguru import logger
import os
import sys
import json
import importlib.util
from flask_swagger_ui import get_swaggerui_blueprint
import shutil
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
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config', 'api.json')
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load config from {config_path}: {e}")
        sys.exit(1)

config = load_config()
strategies_folder = r"api/strategies"
strategies = {}

def reload_loguru_config():
    logger.remove()
    logger.add(sys.stdout, level="DEBUG")
    if config['server']['debug']:
        logger.add(r"logs/api/debug.log", level="DEBUG")
    else:
        logger.add(r"logs/api/logs.log", level="INFO")

def import_signals_and_indicators(strategies_folder="strategies"):
    strategies = {}
    for root, dirs, files in os.walk(strategies_folder):
        for file_name in files:
            if file_name.endswith(".py"):
                file_path = os.path.join(root, file_name)
                name_without_extension = os.path.splitext(file_name)[0]
                strategy_name = os.path.relpath(file_path, strategies_folder).replace(
                    os.sep, '_').rsplit('.', 1)[0]
                try:
                    spec = importlib.util.spec_from_file_location(
                        name_without_extension, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                    buy_signal_func = getattr(module, 'buy_signal', None)
                    sell_signal_func = getattr(module, 'sell_signal', None)
                    indicators_class = getattr(module, 'Indicators', None)
                    if buy_signal_func and sell_signal_func and indicators_class:
                        strategies[strategy_name] = {
                            "buy_signal": buy_signal_func,
                            "sell_signal": sell_signal_func,
                            "Indicators": indicators_class
                        }
                        logger.debug(f"Imported strategy '{strategy_name}' from {file_path}")
                    else:
                        logger.warning(f"Strategy '{strategy_name}' is missing required functions/classes.")
                except Exception as e:
                    logger.error(f"Failed to import module '{strategy_name}' from {file_path}: {e}")
    logger.info(f'Strategies: {strategies}')
    return strategies

def create_app():
    app = Flask(__name__)
    
    # Setup cache
    cache_config = config['cache']
    app.config['CACHE_TYPE'] = cache_config['type']
    app.config['CACHE_DEFAULT_TIMEOUT'] = cache_config['default_timeout']
    cache = Cache(app)
    
    CORS(app, resources={
        r"/QTSBE/*": {
            "origins": ["*"],  # Allow all origins for development
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Accept"],
            "expose_headers": ["Content-Range", "X-Content-Range"]
        }
    })

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    SWAGGER_URL = '/docs'
    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "QTSBE API Documentation"
        }
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    os.makedirs('api/static', exist_ok=True)

    if os.path.exists('swagger.yaml'):
        shutil.copy('swagger.yaml', 'api/static/swagger.yaml')

    register_analyse_routes(app, strategies, analyse)
    register_analyse_custom_routes(app, analyse)
    register_strategy_routes(app, strategies)
    register_get_tokens_routes(app)
    register_get_tokens_stats_routes(app)
    register_health_routes(app)

    return app

if __name__ == '__main__':
    reload_loguru_config()
    strategies = import_signals_and_indicators(strategies_folder)
    logger.debug("List of all strategies: {}", list(strategies.keys()))
    logger.warning("API has been restarted.")
    app = create_app()
    
    port = int(os.getenv('FLASK_QTSBE_PORT', config['server']['port']))
    host = os.getenv('FLASK_HOST', config['server']['host'])
    debug = os.getenv('FLASK_DEBUG', str(config['server']['debug'])).lower() == 'true'
    
    app.run(
        host=host,
        port=port,
        debug=debug
    )
