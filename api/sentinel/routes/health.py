"""Health check and system routes."""
from flask import Blueprint, jsonify

health_bp = Blueprint('health', __name__, url_prefix='/api')


@health_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for Google Cloud Run."""
    return jsonify({"status": "healthy"}), 200
