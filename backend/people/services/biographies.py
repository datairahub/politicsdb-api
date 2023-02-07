# -*- coding: utf-8 -*-
from urllib.parse import urlparse
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
        name=urlparse(url).netloc,
        bio=bio,
    ).save()
