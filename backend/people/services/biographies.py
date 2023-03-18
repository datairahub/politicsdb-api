# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from people.models import Person, BiographySource


def register_biography_source(person: Person, url: str, value: str) -> None:
    """
    Register biography source

    :param person: Person instance
    :param url: source url
    :param value: biography
    """
    if BiographySource.objects.filter(person=person, url=url).exists():
        return

    BiographySource(
        person=person,
        url=url,
        name=urlparse(url).netloc,
        value=value,
    ).save()
