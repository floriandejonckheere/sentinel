"""Assessment API routes."""
import os
import json
import re

from flask import Blueprint, jsonify, request

from sentinel.constants.roles import VALID_ROLE_IDS
from sentinel.constants.sizes import VALID_SIZE_IDS
from sentinel.constants.risk import VALID_RISK_KEYS
from cli.application_info import get_application_info
from cli.assessor import Assessor
from cli.runner import Runner
from cli.tools.trust_score_engine import TrustScoreEngine

assessments_bp = Blueprint('assessments', __name__, url_prefix='/api')

# In-memory storage for assessments (replace with database later)
assessments_store = {}


def parameterize(text: str) -> str:
    """Convert text to a URL-friendly slug (lowercase, hyphenated)."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special characters with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


@assessments_bp.route("/assessments", methods=["GET"])
def list_assessments():
    """List all assessments."""
    return jsonify(list(assessments_store.values())), 200


@assessments_bp.route("/assessments", methods=["POST"])
def create_assessment():
    """Create a new assessment with name or url."""
    data = request.get_json()

    name = data.get("name")
    url = data.get("url")
    if not name and not url:
        return jsonify({"error": "'name' or 'url' must be provided."}), 400

    role = data.get("role")
    if not role:
        return jsonify({"error": "'role' must be provided."}), 400
    if role not in VALID_ROLE_IDS:
        return jsonify({"error": f"Invalid role. Must be one of: {', '.join(sorted(VALID_ROLE_IDS))}"}), 400

    size = data.get("size")
    if not size:
        return jsonify({"error": "'size' must be provided."}), 400
    if size not in VALID_SIZE_IDS:
        return jsonify({"error": f"Invalid size. Must be one of: {', '.join(sorted(VALID_SIZE_IDS))}"}), 400

    risk = data.get("risk")
    if not risk:
        return jsonify({"error": "'risk' must be provided."}), 400
    if risk not in VALID_RISK_KEYS:
        return jsonify({"error": f"Invalid risk. Must be one of: {', '.join(sorted(VALID_RISK_KEYS))}"}), 400

    # Get application information
    input_text = name if name else url
    app_info = get_application_info(input_text)

    # Generate deterministic ID based on parameterized app info
    parameterized_name = parameterize(app_info.name)
    parameterized_vendor = parameterize(app_info.vendor_name)
    assessment_id = f"{parameterized_name}_{parameterized_vendor}"

    # Fetch the cached assessment if it exists
    cache_path = os.path.join("/data", f"{assessment_id}.json")
    if os.path.exists(cache_path):
        return jsonify({"id": assessment_id}), 201

    # TODO: Run the full assessment process here (omitted for brevity)
    runner = Runner(assessment_id=assessment_id, name=input_text)
    runner.run()

    # Return just the ID
    return jsonify({"id": assessment_id}), 201


@assessments_bp.route("/assessments/<assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    """Get a specific assessment by ID."""
    # Check cache first
    cache_path = os.path.join("/data", f"{assessment_id}.json")
    if os.path.exists(cache_path):
        with open(cache_path, "r") as f:
            assessment = json.load(f)
        return jsonify(assessment), 200

    # Return 404 if not found
    return jsonify({"error": "Assessment not found"}), 404
