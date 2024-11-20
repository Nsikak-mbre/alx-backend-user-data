#!/usr/bin/env python3
"""
User class
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User class
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), nullable=False)
    hashed_password = db.Column(db.String(250), nullable=False, unique=True)
    session_id = db.Column(db.String(250), nullable=True)
    reset_token = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        """A string representation of the object"""
        return f'<User {self.email}>'
