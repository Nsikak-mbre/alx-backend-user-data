#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models.user import User
from typing import List, Type


class Auth:
    """Auth class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Presently return false for all paths
        """
        return False
    
    def authorization_header(self, request=None) -> str:
        """Return None for now
        """
        return None
    
    def current_user(self, request=None) -> Type[User]:
        """Return None for now
        """
        return None