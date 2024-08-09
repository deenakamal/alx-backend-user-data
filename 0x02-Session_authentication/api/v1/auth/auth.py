#!/usr/bin/env python3
"""Defines class Auth"""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False if path matches any in excluded_paths,
        True otherwise."""
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if not path.endswith('/'):
            path = path + '/'

        for excluded_path in excluded_paths:
            if (excluded_path.endswith('*')
                    and path.startswith(excluded_path[:-1])):
                return False

            if path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get authrization header"""
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Returns the session cookie value from the request.

        Args:
            request: The request object.

        Returns:
            str: The value of the session cookie, or None if not found.
        """
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
