#!/usr/bin/env python3
"""
Module for filtering log data to obfuscate specified fields.
"""

import re
from typing import List


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
