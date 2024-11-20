#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional


class Auth:
    """
    Auth class to manage the authentication system
    """

    def _has_password(self, password: str) -> bytes:
        """Hash a password
        Args:
            password (str): The password to hash.
        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password
