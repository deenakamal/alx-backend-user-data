#!/usr/bin/env python3
"""Module"""
from .base import Base


class UserSession(Base):
    """UserSession class"""
    def __init__(self, *args: list, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
