"""Assessment API routes."""
import uuid
import os
from datetime import datetime

from flask import Blueprint, jsonify, request

from sentinel.constants.roles import VALID_ROLE_IDS
from sentinel.constants.sizes import VALID_SIZE_IDS
from sentinel.constants.risk import VALID_RISK_KEYS

assessments_bp = Blueprint('assessments', __name__, url_prefix='/api')

# In-memory storage for assessments (replace with database later)
assessments_store = {}


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

    # Generate unique ID for this assessment
    assessment_id = str(uuid.uuid4())

    # TODO: Use CLI assessor to perform actual assessment (after merge)
    # from cli.assessor import Assessor
    # from cli.database import Database
    # from cli.ai import AI
    # db = Database("sqlite:///data/sentinel.sqlite3")
    # ai = AI()
    # assessor = Assessor(database=db, ai=ai)
    # assessment = assessor.assess(name=name, url=url)

    # Return just the ID
    return jsonify({"id": assessment_id}), 201


@assessments_bp.route("/assessments/<assessment_id>", methods=["GET"])
def get_assessment(assessment_id):
    """Get a specific assessment by ID."""
    return open(os.path.join(os.path.dirname(__file__), "example_assessment.json")).read(), 200
