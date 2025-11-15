import os
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS


def create_app():
    """Create and configure the Sentinel Flask application."""
    # Set static folder to serve built frontend at /app/
    static_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
    # Don't set static_url_path - we'll manually handle all /app/ routes
    app = Flask(__name__, static_folder=static_folder, static_url_path=None)

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # API Routes (all under /api/)
    @app.route("/api/health", methods=["GET"])
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

        # TODO: Use CLI assessor to perform actual assessment (after merge)
        # from cli.assessor import Assessor
        # from cli.database import Database
        # from cli.ai import AI
        # db = Database("sqlite:///data/sentinel.sqlite3")
        # ai = AI()
        # assessor = Assessor(database=db, ai=ai)
        # assessment = assessor.assess(name=name, url=url)
        # return jsonify(assessment.to_json()), 200

        return jsonify({
            "name": name,
            "url": url
        }), 200

    # Redirect root to /app/
    @app.route('/')
    def redirect_to_app():
        """Redirect root to /app/."""
        from flask import redirect
        return redirect('/app/', code=302)

    # Frontend Routes - Serve React app under /app/
    # This catches ALL routes under /app/ for client-side routing
    @app.route('/app/', defaults={'path': ''})
    @app.route('/app/<path:path>')
    def serve_frontend(path):
        """Serve the React frontend application at /app/."""
        # If path exists as a static file (js, css, images, etc.), serve it
        if path:
            file_path = os.path.join(app.static_folder, path)
            if os.path.isfile(file_path):
                return send_from_directory(app.static_folder, path)

        # Otherwise, serve index.html for client-side routing
        # This handles routes like /app/name, /app/role, etc.
        return send_from_directory(app.static_folder, 'index.html')

    return app
