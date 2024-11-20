#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import User, Base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import bcrypt

from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database.
        Args:
            email (str): The user's email address.
            hashed_password (str): The user's hashed password.
        Returns:
            User: The created user instance.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute
        Args:
            **kwargs: Arbitrary keyword arguments.
        Returns:
            User: The user found or raises an exception if not found.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No result found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid request")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update a user in the database
        Args:
            user_id (int): The user ID.
            **kwargs: Arbitrary keyword arguments.
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError("No result found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError("User has no attribute {}".format(key))
            setattr(user, key, value)
        self._session.commit()

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
