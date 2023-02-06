# -*- coding: utf-8 -*-
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
        is_exact=is_exact,
        date=date,
    ).save()
