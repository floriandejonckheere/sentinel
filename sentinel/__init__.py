import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


def create_app():
    """Create and configure the Sentinel Flask application (root package)."""
    # Built frontend lives under api/static after Docker build
    static_folder = os.path.join(os.path.dirname(__file__), '..', 'api', 'static')
    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "healthy"}), 200

    @app.route("/api/assessments", methods=["GET"])
    def list_assessments():
        return jsonify([]), 200

    @app.route("/api/assessments", methods=["POST"])
    def create_assessment():
        data = request.get_json() or {}
        name = data.get("name")
        url = data.get("url")
        # Example usage of merged CLI (kept commented until wired)
        # from cli.assessor import Assessor
        # from cli.database import Database
        # from cli.ai import AI
        # db = Database("sqlite:///sentinel.sqlite3")
        # ai = AI()
        # assessor = Assessor(database=db, ai=ai)
        # assessment = assessor.assess(name=name, url=url)
        # return jsonify(assessment.to_json()), 200
        return jsonify({"name": name, "url": url}), 200

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path.startswith('api/') or path == 'health':
            return jsonify({"error": "Not found"}), 404
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')

    return app
