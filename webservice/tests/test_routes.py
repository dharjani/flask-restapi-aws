from flask import Flask
from ..routes.healthcheck_routes import healthcheck_routes

def test_healthcheck_route():
    app = Flask(__name__)
    app.register_blueprint(healthcheck_routes)
    client = app.test_client()
    response=client.get('/healthz')
    assert response.status_code == 200
