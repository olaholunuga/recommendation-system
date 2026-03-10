import pytest
from app import create_app

@pytest.fixture()
def app():
    # Create the app instance
    app = create_app()
    # Enable testing mode, which disables error trapping and routes exceptions properly
    app.config.update({
        "TESTING": True,
    })
    yield app

@pytest.fixture()
def client(app):
    # Return a test client that can make simulated HTTP requests
    return app.test_client()