#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, Type
from models.user import User


class Auth:
    """Auth class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth
        """
        return False

    def authorization_header(self) -> str:
        """Authorization header
        """
        return None

    def current_user(self, request=None) -> Type[User]:
        """Current user
        """
        return None
