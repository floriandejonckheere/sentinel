from flask import Flask, jsonify


def create_app():
    """Create and configure the Sentinel Flask application."""
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint for Google Cloud Run."""
        return jsonify({"status": "healthy"}), 200

    return app
