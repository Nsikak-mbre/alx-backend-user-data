#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from typing import Optional
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a Password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """
    Auth class to interact with the database
    """
    def __init__(self):
        """
        Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            User: The created user instance.

        Raises:
            ValueError: If the user already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            pass
        hashed_password = _hash_password(password)
        new_user = self._db.add_user(email, hashed_password)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials

        Args:
            email (str): The user's email address.
            password (str): The user's password.

        Returns:
            bool: True if the user's password is correct, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
        except NoResultFound:
            pass
        return False
