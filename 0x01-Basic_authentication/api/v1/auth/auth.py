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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Ensure path ends with /
        if not path.endswith('/'):
            path += '/'

        # Ensure path is not in excluded_paths
        if path in excluded_paths:
            return False

        return True

    def authorization_header(self) -> str:
        """Authorization header
        """
        return None

    def current_user(self, request=None) -> Type[User]:
        """Current user
        """
        return None
