#!/usr/bin/env python3
"""
User class
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional

Base = declarative_base()


class User(Base.Model):
    """
    User class
    """
    __tablename__: str = 'users'
    id = Base.Column(Base.Integer, primary_key=True)
    email = Base.Column(Base.String(250), nullable=False)
    hashed_password = Base.Column(Base.String(250), nullable=False)
    session_id = Base.Column(Base.String(250), nullable=True)
    reset_token = Base.Column(Base.String(250), nullable=True)
