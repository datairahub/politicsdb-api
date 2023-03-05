# -*- coding: utf-8 -*-
from django.db.models import F

from core.cache import cached_stats
from positions import models, serializers
from people.models import Person


@cached_stats(base="INSTITUTION_AGES")
def get_institution_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution age stats
    """
    instance = models.Institution.objects.get(pk=pk)
    query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        birth_date__isnull=False,
    )

    if params.get("genre"):
        query = query.filter(genre=params.get("genre"))

    query = query.annotate(
        position_start=F("positions__start"),
        position_end=F("positions__end"),
    )

    data = {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "positions": serializers.InstitutionAgeStatsSerializer(query, many=True).data,
    }
    return data
