from flask import Flask, jsonify, request


def create_app():
    """Create and configure the Sentinel Flask application."""
    app = Flask(__name__)

    @app.route("/health", methods=["GET"])
    def health_check():
        """Health check endpoint for Google Cloud Run."""
        return jsonify({"status": "healthy"}), 200

    @app.route("/assessments", methods=["POST"])
    def create_assessment():
        """Create a new assessment with name or url."""
        data = request.get_json()

        name = data.get("name")
        url = data.get("url")

        return jsonify({
            "name": name,
            "url": url
        }), 200

    return app
