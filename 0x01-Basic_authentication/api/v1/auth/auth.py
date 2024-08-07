#!/usr/bin/env python3
"""Defines class Auth"""
from flask import request
from typing import List, TypeVar


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

        header = request.headers.get('Authorization')
        if not header:
            return None

        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """Returns None"""
        return None
