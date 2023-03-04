# -*- coding: utf-8 -*-
from django.db.models import F
from django.core.cache import cache

from positions import models, serializers
from people.models import Person


def get_institution_age_stats(institution_id: str) -> dict:
    """
    Return institution age stats
    """
    if cache.get(f"INSTITUTION_{institution_id}_AGES"):
        return cache.get(f"INSTITUTION_{institution_id}_AGES")

    instance = models.Institution.objects.get(pk=institution_id)
    persons = (
        Person.objects.prefetch_related(
            "positions",
            "positions__period",
            "positions__period__institution",
        )
        .filter(
            positions__period__institution_id=institution_id,
            birth_date__isnull=False,
        )
        .annotate(
            position_start=F("positions__start"),
            position_end=F("positions__end"),
        )
    )

    data = {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "positions": serializers.InstitutionAgeStatsSerializer(persons, many=True).data,
    }
    cache.set(f"INSTITUTION_{institution_id}_AGES", data)
    return data
