#!/usr/bin/env python3
"""Session-based authentication module."""

from .auth import Auth
from models.user import User
import uuid


class SessionAuth(Auth):
    """Handles session-based authentication.

    This class manages the creation, storage,
    retrieval, and destruction
    of user sessions using unique session IDs.
    """
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """Initializes a new instance of SessionAuth."""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session ID for the given user ID.

        Args:
            user_id (str): The user ID to create a session for.

        Returns:
            str: A unique session ID, or None if user_id is invalid.
        """
        if not user_id or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves the user ID associated with a given session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The associated user ID, or None
            if session_id is invalid or not found.
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Retrieves the current user based on,
        the session cookie in the request.

        Args:
            request: The request object containing the session cookie.

        Returns:
            User: The User instance associated with the session,
            or None if not found.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """Destroys the session associated with the request.

        Args:
            request: The request object containing the session cookie.

        Returns:
            bool: True if the session was successfully destroyed,
            False otherwise.
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        if session_id in self.user_id_by_session_id:
            del self.user_id_by_session_id[session_id]
        return True
