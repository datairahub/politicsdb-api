# -*- coding: utf-8 -*-
from urllib.parse import urlparse
from people.models import BirthDateSource


def register_birth_date_source(person, url, date, is_exact):
    """
    Register birth date source
    """
    if BirthDateSource.objects.filter(person=person, url=url).exists():
        return

    BirthDateSource(
        person=person,
        url=url,
        name=urlparse(url).netloc,
        is_exact=is_exact,
        date=date,
    ).save()

    if not person.birth_date:
        person.birth_date = date
        person.save(update_fields=["birth_date"])
