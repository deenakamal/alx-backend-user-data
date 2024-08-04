#!/usr/bin/env python3
""" Module """
import bcrypt


def hash_password(password) -> str:
    """Returned Hashed password """
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def is_valid(hash_password: bytes, password: str) -> bool:
    """to validates that the provided password matches the hashed password"""
    check_ = bcryp.hashpw(password.encode('utf-8'), hashed_password)
