#!/usr/bin/env python3
""" Module """
import re
form typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns the log message obfuscated. """
    for field in fields:
        pattren = rf"{field}=.*?{separator}"
        replacement = f"{redaction}{separator}"
        message = re.sub(pattern. replacement, message)

        return message
