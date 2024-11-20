#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from typing import Optional
from db import DB


def _hash_password(password: str) -> bytes:
    """
    Hash a Password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
