#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response, abort, redirect
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """
    Log out a user and delete their session.

    Request:
    - A "session_id" cookie containing the user's session ID.

    Response:
    - On success, return a JSON payload.
    - On failure, abort with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")

    # validate session
    if not session_id:
        abort(403)

    # find the user by session_id
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if not user:
        abort(403)

    # destroy session
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """
    Get the profile of the current user.

    Request:
    - A "session_id" cookie containing the user's session ID.

    Response:
    - On success, return a JSON payload.
    - On failure, abort with a 403 HTTP status.
    """
    session_id = request.cookies.get("session_id")

    # validate session
    if not session_id:
        abort(403)

    # find the user by session_id
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({'email': user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get a reset password token for a user

    Request:
    - Form data containing "email"

    Response:
    - On success, return a JSON payload.
    - On failure, abort with a 403 HTTP status.
    """
    email = request.form.get("email")

    # validate form data
    if not email:
        abort(403)

    # generate reset token
    try:
        token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort
    # Return the reset token and email
    return jsonify({'email': email, 'reset_token': token}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
