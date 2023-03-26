# -*- coding: utf-8 -*-
import re
from datetime import date
from django.core.exceptions import ValidationError


def validate_partial_date(value: str):
    """
    Validate partial date. Admited formats:
    - YYYY
    - YYYY-MM
    - YYYY-MM-DD
    """
    if len(value) == 4:
        value += "-01-01"
    elif len(value) == 7:
        value += "-01"
    try:
        date.fromisoformat(value)
    except ValueError:
        raise ValidationError(
            "Incorrect date format, should be YYYY or YYYY-MM or YYYY-MM-DD"
        )


def validate_hex_color(value: str):
    """
    Validate hexadecimal color (#FF0000)
    - #FFF not allowed
    """
    match = re.search(r"^#[0-9A-F]{6}$", str)
    if not match:
        raise ValidationError("Incorrect color format, should be #OOOOOO (# + 6 chars)")
