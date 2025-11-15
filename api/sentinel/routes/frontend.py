"""Frontend serving routes."""
import os
from flask import Blueprint, send_from_directory, redirect, current_app

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/')
def redirect_to_app():
    """Redirect root to /app/."""
    return redirect('/app/', code=302)


@frontend_bp.route('/app/', defaults={'path': ''})
@frontend_bp.route('/app/<path:path>')
def serve_frontend(path):
    """Serve the React frontend application at /app/."""
    static_folder = current_app.static_folder

    # If path exists as a static file (js, css, images, etc.), serve it
    if path:
        file_path = os.path.join(static_folder, path)
        if os.path.isfile(file_path):
            return send_from_directory(static_folder, path)

    # Otherwise, serve index.html for client-side routing
    # This handles routes like /app/name, /app/role, etc.
    return send_from_directory(static_folder, 'index.html')
