# -*- coding: utf-8 -*-
from datetime import date
from urllib.parse import urlparse
from people.models import Person, BirthDateSource


def register_birth_date_source(person: Person, url: str, value: str) -> None:
    """
    Register birth date source

    :param person: Person instance
    :param url: source url
    :param value: date
    """
    name = urlparse(url).netloc
    birth_date = value
    accuracy = 3

    if len(value) == 7:
        birth_date = f"{value}-01"
        accuracy = 2
    elif len(value) == 4:
        birth_date = f"{value}-01-01"
        accuracy = 1

    try:
        birth_date = date.fromisoformat(birth_date)
    except Exception:
        return

    registered = BirthDateSource.objects.filter(person=person, name=name).first()
    if registered and registered.accuracy >= accuracy:
        return

    if registered:
        registered.value = value
        registered.date = birth_date
        registered.accuracy = accuracy

    else:
        BirthDateSource(
            person=person,
            url=url,
            name=name,
            value=value,
            date=birth_date,
            accuracy=accuracy,
        ).save()

    if (
        not person.birth_date
        or not person.birth_date_accuracy
        or accuracy > person.birth_date_accuracy
    ):
        person.birth_date = birth_date
        person.birth_date_accuracy = accuracy
        person.save(update_fields=["birth_date", "birth_date_accuracy"])
