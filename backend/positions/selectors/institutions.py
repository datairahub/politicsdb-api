# -*- coding: utf-8 -*-
from django.db.models import F, Avg

from core.cache import cached_stats
from positions import models, serializers
from people.models import Person


@cached_stats(base="INSTITUTION_DISTRIBUTION_AGE")
def get_institution_distribution_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution distribution age stats

    :param pk: institution primary key
    :param params: filter params
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

    return {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "positions": serializers.InstitutionDistributionAgeSerializer(
            query, many=True
        ).data,
    }


@cached_stats(base="INSTITUTION_MEAN_AGE")
def get_institution_mean_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution mean age stats

    :param pk: institution primary key
    :param params: filter params
    """
    instance = models.Institution.objects.get(pk=pk)

    query = models.Period.objects.prefetch_related(
        "positions",
        "positions__person",
    ).filter(
        institution=instance,
        positions__person__birth_date__isnull=False,
    )

    if params.get("genre"):
        query = query.filter(positions__person__genre=params.get("genre"))

    query = query.values("id", "name", "start", "end").annotate(
        mean_age=Avg(F("positions__start") - F("positions__person__birth_date"))
    )

    if params.get("split") and params.get("split") == "genre":
        query = query.annotate(genre=F("positions__person__genre"))

    query = query.order_by("id")

    return {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "periods": serializers.InstitutionMeanAgeSerializer(query, many=True).data,
    }
