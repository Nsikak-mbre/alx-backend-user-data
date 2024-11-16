#!/usr/bin/env python3
"""
Basic Auth module
"""
from api.v1.auth.auth import Auth
from typing import Type, Tuple, TypeVar
from models.user import User
import base64


class BasicAuth(Auth):
    """BasicAuth class that inherits from Auth
    """

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extract base64 authorization header
        """
        if authorization_header is None or type(
                authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[len("Basic "):]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decode base64 authorization header
        """
        if base64_authorization_header is None or type(
                base64_authorization_header) is not str:
            return None
        try:
            return base64.b64decode(
                base64_authorization_header.encode('utf-8')).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """Extract user credentials from the decoded Bsae64 authorization
        header
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None

        # split only at the first occurence of ':'
        try:
            email, password = decoded_base64_authorization_header.split(':', 1)
            return email, password
        except ValueError:
            return None, None

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> 'User':
        """User object from credentials
        """
        if user_email is None or user_pwd is None:
            return None
        if not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        try:
            user = User.search({'email': user_email})
            if user is None or len(user) == 0:
                return None
            user = user[0]
            if not user.is_valid_password(user_pwd):
                return None
            return user
        except Exception:
            return None
