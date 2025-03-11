#!/usr/bin/env python3
""" Module of Auth views
"""
from flask import request, jsonify, abort
from typing import List, TypeVar

class Auth:
    """
    Authentication class
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Method that require authentication
        """
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path in excluded_paths:
            return False
        
        return True
    
    def authorization_header(self, request=None) -> str:
        """ Handles authorization header
        """
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Handles current user
        """
        return None
