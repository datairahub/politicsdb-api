# -*- coding: utf-8 -*-
from people.models import BiographySource


def register_biography_source(person, url, bio):
    """
    Register biography source
    """
    if BiographySource.objects.filter(person=person, url=url).exists():
        return

    BiographySource(
        person=person,
        url=url,
        bio=bio,
    ).save()
