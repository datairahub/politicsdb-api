# -*- coding: utf-8 -*-
from django.apps import apps
from django.conf import settings
from core.cache import cached_value


def get_field_data(field) -> dict:
    """
    Get serialized field data for a field

    :return: field data
    """
    return {
        "name": field.name,
        "verbose_name": field.verbose_name,
        "help_text": field.help_text,
    }


def get_model_fields(model) -> list:
    """
    Get all fields for a model excluding private ones

    :return: model fields
    """
    return [
        get_field_data(field)
        for field in model._meta.fields
        if not field.name in settings.PUBLIC_DATA["EXCLUDED_FIELDS"]
    ]


@cached_value("MODELS_FIELDS")
def get_models_fields_data() -> list:
    """
    Get all models in an already serialized list with
    all their fields, excluding private ones

    :return: models list
    """
    data = []
    for model in apps.get_models():
        label = model._meta.label.split(".")

        if label[0] in settings.PUBLIC_DATA["EXCLUDED_APPS"]:
            continue

        data.append(
            {
                "name": label[1],
                "fields": get_model_fields(model),
                "description": model.__doc__,
            }
        )

    return data
