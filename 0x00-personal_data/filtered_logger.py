#!/usr/bin/env python3
""" Module """
import re
from typing import List
import logging

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ A function that returns the log message obfuscated. """
    for field in fields:
        pattren = rf"{field}=.*?{separator}"
        replacement = f"{field}={redaction}{separator}"
        message = re.sub(pattren, replacement, message)

    return message


def get_logger() -> logging.Logger:
    """get logger """
    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Method to filter values in incoming log records. """
        msg = super(RedactingFormatter, self).format(record)
        msg = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return msg
