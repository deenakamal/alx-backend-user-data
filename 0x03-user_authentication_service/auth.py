#!/usr/bin/env python3
"""Authentication Module"""

from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
import uuid


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user with an email and password.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            User: The newly created user object.
        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email=email,
                                     hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate the user's login credentials.
        Args:
            email (str): The user's email address.
            password (str): The user's password.
        Returns:
            bool: True if the credentials are valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            is_valid_password = bcrypt.checkpw(password.encode('utf-8'),
                                               user.hashed_password)
            return is_valid_password
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Create a new session for the user and return the session ID.

        Args:
            email (str): The user's email address.

        Returns:
            str: The session ID.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieve a user based on the session ID.
        Args:
            session_id (str): The session ID.
        Returns:
            User: The user associated with the session ID.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session.
        Args:
            user_id (int): The user's ID.
        Returns:
            None
        """
        if not user_id:
            return None

        try:
            self._db.update_user(user_id, session_id=None)
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for the user.

        Args:
            email (str): The user's email address.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Update the user's password using the reset token.
        Args:
            reset_token (str): The reset token.
            password (str): The new password.
        Returns:
            None
        Raises:
            ValueError: If the reset token is invalid or expired.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            new_hashed_password = _hash_password(password)
            self._db.update_user(user.id,
                                 hashed_password=new_hashed_password,
                                 reset_token=None)
        except NoResultFound:
            raise ValueError


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """
    Generate a new UUID.

    Returns:
        str: A string representation of a new UUID.
    """
    return str(uuid.uuid4())
