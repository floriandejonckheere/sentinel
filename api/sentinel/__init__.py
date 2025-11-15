import os
from flask import Flask
from flask_cors import CORS

from sentinel.routes.health import health_bp
from sentinel.routes.assessments import assessments_bp
from sentinel.routes.frontend import frontend_bp


def create_app():
    """Create and configure the Sentinel Flask application."""
    # Set static folder to serve built frontend at /app/
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    # Don't set static_url_path - we'll manually handle all /app/ routes
    app = Flask(__name__, static_folder=static_folder, static_url_path=None)

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(health_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(frontend_bp)  # Register last to catch all remaining routes

    return app
