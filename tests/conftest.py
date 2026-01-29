import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../api'))

from api import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()
