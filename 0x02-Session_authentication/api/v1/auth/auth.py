#!/usr/bin/env python3
"""
Auth class
"""
from flask import request
from typing import List, Type
from models.user import User
import logging

logger = logging.getLogger(__name__)


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

    def authorization_header(self, request=None) -> str:
        """Authorization header
        """
        if request is None:
            logger.debug("Request is None")
            return None
        if 'Authorization' not in request.headers:
            logger.debug("Authorization header not found")
            return None
        auth_header = request.headers['Authorization']
        logger.debug("Authorization header: {}".format(auth_header))
        return auth_header

    def current_user(self, request=None) -> Type[User]:
        """Current user
        """
        if request is None:
            logger.debug("Request is None")
            return None

        auth_header = self.authorization_header(request)
        if auth_header is None:
            logger.debug("Authorization header is None")
            return None
        try:
            token = auth_header.split(' ')[1]
            logger.debug("Token: {}".format(token))
        except IndexError:
            logger.debug("Token not found")
            return None

        user_id = User().get_user_from_token(token)
        if user_id is None:
            logger.debug("User ID not found")
            return None
        else:
            logger.debug("User ID: {}".format(user_id))
        return user_id
