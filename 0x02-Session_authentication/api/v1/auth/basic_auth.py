#!/usr/bin/env python3
"""Module"""
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
import base64
from models.user import User


class BasicAuth(Auth):
    """BasicAuth class inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts Base64 part from Authorization header"""
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes Base64 string"""
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            base64_bytes = base64_authorization_header.encode('utf-8')
            decoded_bytes = base64.b64decode(base64_bytes)
            return decoded_bytes.decode('utf-8')
        except (TypeError, base64.binascii.Error):
            return None

    def extract_user_credentials(
                                 self,
                                 decoded_base64_authorization_header: str
                                ) -> Tuple[str, str]:
        """Extracts user email and password from decoded Base64 string"""
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(
            decoded_base64_authorization_header.split(':', 1)
        )

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """Returns a User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User().search({'email': user_email})
        if not users:
            return None

        user = users[0]
        is_valid_pwd = user.is_valid_password(user_pwd)
        if not is_valid_pwd:
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
            auth_header
        )
        decoded_auth_header = self.decode_base64_authorization_header(
            base64_auth_header
        )
        email, password = self.extract_user_credentials(decoded_auth_header)
        return self.user_object_from_credentials(email, password)
