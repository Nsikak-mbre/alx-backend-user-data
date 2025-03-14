#!/usr/bin/env python3
"""
Module for filtering log data to obfuscate specified fields.
"""

import re
import logging
import mysql.connector
from mysql.connector.connection import MySQLConnection
from typing import List
import os


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates specified fields in a log message.

    Args:
        fields (List[str]): Fields to be obfuscated.
        redaction (str): The string to replace the field values with.
        message (str): The log message to process.
        separator (str): The field separator in the log message.

    Returns:
        str: The log message with obfuscated fields.
    """
    escaped_fields = [re.escape(field) for field in fields]
    joined_fields = '|'.join(escaped_fields)
    pattern = f"({joined_fields})=.+?{re.escape(separator)}"

    return re.sub(
        pattern, lambda m: f"{m.group(1)}={redaction}{separator}", message)


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class to filter sensitive information."""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the RedactingFormatter with specific fields to redact.

        Args:
            fields (List[str]): List of fields to redact.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Redact sensitive information from log records.

        Args:
            record (logging.LogRecord): Log record to format.

        Returns:
            str: The formatted log record with redacted fields.
        """
        original_message = super().format(record)
        return filter_datum(self.fields, self.REDACTION,
                            original_message, self.SEPARATOR)


def get_logger() -> logging.Logger:
    """
    Create and return a logging.Logger object.

    Returns:
        logging.Logger: The created logger object.
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def get_db() -> MySQLConnection:
    """
    Connect to a MySQL database and return the connection object.

    Returns:
        MySQLConnection: The
    """
    return mysql.connector.connect(
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME"),
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""))
