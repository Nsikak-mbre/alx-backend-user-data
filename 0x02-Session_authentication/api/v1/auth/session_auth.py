#!/usr/bin/env python3
"""
Session Authentication module
"""
from api.v1.auth.auth import Auth
from models.user import User
from flask import request

class SessionAuth(Auth):
    """ SessionAuth class
    """
    pass