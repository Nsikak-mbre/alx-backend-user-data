#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
import uuid
from typing import Optional
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a Password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """
    Generate a UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """
        create a session ID for a user.

        Args:
            email (str): The user's email address.
        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get a user from a session ID
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None
        except ValueError:
            return None
        except InvalidRequestError:
            return None
        return None

    def destroy_session(self, user_id: int) -> None:
        """ Destroy a user's session.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Get a reset password token for a user

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset password token.

        Raises:
            ValueError: If the user does not exist.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("Email not found")
        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)
        return token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password

        Args:
            reset_token (str): The reset password token.
            password (str): The user's new password.

        Raises:
            ValueError: If the token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None)
        return None

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update a user's password

        Args:
            reset_token (str): The reset password token.
            password (str): The user's new password.

        Raises:
            ValueError: If the token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = self._hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None)
        return None
