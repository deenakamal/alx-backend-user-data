#!/usr/bin/env python3
"""Main module to test user authentication service"""

import requests

BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """Register a new user"""
    url = f"{BASE_URL}/users"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")
    assert (response.json() == {"email": email, "message": "user created"},
            f"Unexpected response: {response.json()}")


def log_in_wrong_password(email: str, password: str) -> None:
    """Attempt to log in with wrong password"""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert (response.status_code == 401,
            f"Expected status code 401, but got {response.status_code}")


def log_in(email: str, password: str) -> str:
    """Log in with correct credentials and return session ID"""
    url = f"{BASE_URL}/sessions"
    payload = {"email": email, "password": password}
    response = requests.post(url, data=payload)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")
    session_id = response.cookies.get("session_id")
    assert session_id is not None, "No session_id found in response"
    return session_id


def profile_unlogged() -> None:
    """Attempt to access profile without being logged in"""
    url = f"{BASE_URL}/profile"
    response = requests.get(url)
    assert (response.status_code == 403,
            f"Expected status code 403, but got {response.status_code}")


def profile_logged(session_id: str) -> None:
    """Access profile while logged in"""
    url = f"{BASE_URL}/profile"
    cookies = {"session_id": session_id}
    response = requests.get(url, cookies=cookies)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")


def log_out(session_id: str) -> None:
    """Log out from the session"""
    url = f"{BASE_URL}/sessions"
    cookies = {"session_id": session_id}
    response = requests.delete(url, cookies=cookies)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")


def reset_password_token(email: str) -> str:
    """Request a password reset token"""
    url = f"{BASE_URL}/reset_password"
    payload = {"email": email}
    response = requests.post(url, data=payload)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")
    reset_token = response.json().get("reset_token")
    assert reset_token is not None, "No reset_token found in response"
    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Update password using the reset token"""
    url = f"{BASE_URL}/reset_password"
    payload = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(url, data=payload)
    assert (response.status_code == 200,
            f"Expected status code 200, but got {response.status_code}")
    assert (response.json() == {"email": email, "message": "Password updated"},
            f"Unexpected response: {response.json()}")


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
