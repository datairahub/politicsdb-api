# -*- coding: utf-8 -*-
from people.models import BirthSource


def register_birth_date_source(person, url, date, is_exact):
    """
    Register birth date source
    """
    if BirthSource.objects.filter(person=person, url=url).exists():
        return

    BirthSource(
        person=person,
        url=url,
        is_exact=is_exact,
        date=date,
    ).save()
