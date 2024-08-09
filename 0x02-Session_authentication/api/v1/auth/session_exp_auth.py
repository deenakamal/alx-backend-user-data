#!/usr/bin/env python3
""" module of session_exp_auth
"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from typing import TypeVar
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """SessionExpAuth class"""

    def __init__(self):
        """constructor"""
        self.session_duration = int(getenv("SESSION_DURATION", 0))

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration <= 0:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary:
            return None
        created_at = session_dictionary.get("created_at")
        if created_at is None:
            return None
        if (created_at + timedelta(seconds=self.session_duration)) \
                < datetime.now():
            return None
        return session_dictionary.get("user_id")
