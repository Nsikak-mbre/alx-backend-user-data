#!/usr/bin/env python3
"""
Route module for the API
"""
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os
from os import getenv
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# create variable auth initialized to None
auth = None

# Based on the value of the environment variable AUTH_TYPE,
# import the appropriate Auth class
auth_type = os.getenv("AUTH_TYPE")

if auth_type == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def handle_unauthorized(error):
    """Return JSON response for 401 Unauthorized error."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def handle_forbidden(error):
    """Return JSON response for 403 Forbidden error."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request():
    """Handle before request."""
    if auth is None:
        logger.debug("auth is None")
        # api/v1/app.py


@app.before_request
def before_request():
    """Request filtering based on authentication requirements."""
    if auth is None:
        logger.debug("Auth is None, bypassing.")
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        logger.debug(f"Path '{request.path}' does not require auth.")
        return

    if auth.authorization_header(request) is None:
        logger.warning("Authorization header is missing.")
        abort(401)

    if auth.current_user(request) is None:
        logger.warning("User authentication failed.")
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
