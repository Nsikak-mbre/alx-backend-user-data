#!/usr/bin/env python3

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
