# -*- coding: utf-8 -*-
from datetime import date
from urllib.parse import urlparse
from people.models import Person, DeathDateSource


def register_death_date_source(person: Person, url: str, value: str) -> None:
    """
    Register death date source

    :param person: Person instance
    :param url: source url
    :param value: date
    """
    name = urlparse(url).netloc
    death_date = value
    accuracy = 3

    if len(value) == 7:
        death_date = f"{value}-01"
        accuracy = 2
    elif len(value) == 4:
        death_date = f"{value}-01-01"
        accuracy = 1

    try:
        death_date = date.fromisoformat(death_date)
    except Exception:
        return

    registered = DeathDateSource.objects.filter(person=person, name=name).first()
    if registered and registered.accuracy >= accuracy:
        return

    if registered:
        registered.value = value
        registered.date = death_date
        registered.accuracy = accuracy

    else:
        DeathDateSource(
            person=person,
            url=url,
            name=name,
            value=value,
            date=death_date,
            accuracy=accuracy,
        ).save()

    if (
        not person.death_date
        or not person.death_date_accuracy
        or accuracy > person.death_date_accuracy
    ):
        person.death_date = death_date
        person.death_date_accuracy = accuracy
        person.save(update_fields=["death_date", "death_date_accuracy"])
