# -*- coding: utf-8 -*-
import re
from unidecode import unidecode


def remove_double_whitespaces(text: str) -> str:
    """
    Remove double whitespaces from strings

    :param text: input text
    :return: clean text
    """
    while "  " in text:
        text = text.replace("  ", " ")
    return text.strip()


def people_id_from_name(name: str) -> str:
    """
    Transform person full name to snakecase to use as ID

    :param name: person full name
    :return: snake_case name
    """
    rm_pattern = re.compile(r"\b\w{1,2}\b")
    hp_pattern = re.compile(r"[\W_]+")
    name = remove_double_whitespaces(name.lower())
    name = unidecode(name)
    name = rm_pattern.sub("", name)
    name = remove_double_whitespaces(name)
    name = hp_pattern.sub("_", name.strip())
    return name.strip()
