# -*- coding: utf-8 -*-
from django.core.exceptions import ValidationError


def adm_flag_path(instance, filename: str) -> str:
    """
    Generate Adm flag path
    """
    model = instance._meta.model.__name__.lower()
    return f"static/images/{model}/{instance.id}.png"


def validate_flag_filetype(value):
    if value.file.content_type != "image/png":
        raise ValidationError("Image must be a PNG file")
