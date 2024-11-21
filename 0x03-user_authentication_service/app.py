#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def hello_world():
    """Return a friendly HTTP greeting."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Register a new user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({'email': user.email, 'message': 'user created'})
    except ValueError as err:
        return jsonify({'message': "email already registerd"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """
    Log in a user and create a session.

    Request:
    - Form data containing "email" and "password"

    Response:
    - On success, set a "session_id" cookie and return a JSON payload.
    - On failure, abort with a 401 HTTP status.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    # validate form data
    if not email or not password:
        abort(401)

    # validate login
    if not AUTH.valid_login(email, password):
        abort(401)

    # create session
    session_id = AUTH.create_session(email)
    if not session_id:
        abort(401)

    # create response
    response = make_response(jsonify({'email': email, 'message': 'logged in'}))
    response.set_cookie('session_id', session_id)
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
