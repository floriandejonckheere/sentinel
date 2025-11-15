import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


def create_app():
    """Create and configure the Sentinel Flask application."""
    # Set static folder to serve built frontend
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # API Routes
    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint for Google Cloud Run."""
        return jsonify({"status": "healthy"}), 200

    @app.route("/api/assessments", methods=["GET"])
    def list_assessments():
        """List all assessments."""
        return jsonify([]), 200

    @app.route("/api/assessments", methods=["POST"])
    def create_assessment():
        """Create a new assessment with name or url."""
        data = request.get_json()

        name = data.get("name")
        url = data.get("url")

        # TODO: Use CLI assessor to perform actual assessment
        # from assessor import Assessor
        # from database import Database
        # from ai import AI
        #
        # db = Database("sqlite:///sentinel.sqlite3")
        # ai = AI()
        # assessor = Assessor(database=db, ai=ai)
        # assessment = assessor.assess(name=name, url=url)
        # return jsonify(assessment.to_json()), 200

        return jsonify({
            "name": name,
            "url": url
        }), 200

    # Frontend Routes - Serve React app for all non-API routes
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        """Serve the React frontend application."""
        # Skip API and health routes
        if path.startswith('api/') or path == 'health':
            return jsonify({"error": "Not found"}), 404

        # Serve static files if they exist
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)

        # Otherwise serve index.html (for client-side routing)
        return send_from_directory(app.static_folder, 'index.html')

    return app
