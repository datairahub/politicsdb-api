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
    positions_query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        birth_date__isnull=False,
    )
    none_query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        birth_date__isnull=True,
    )

    if params.get("genre"):
        positions_query = positions_query.filter(genre=params.get("genre"))
        none_query = none_query.filter(genre=params.get("genre"))

    positions_query = positions_query.annotate(
        position_start=F("positions__start"),
        position_end=F("positions__end"),
    )

    return {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "positions": serializers.InstitutionDistributionAgeSerializer(
            positions_query,
            many=True,
        ).data,
        "no_date": none_query.count(),
    }


@cached_stats(base="INSTITUTION_MEAN_AGE")
def get_institution_mean_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution mean age stats

    :param pk: institution primary key
    :param params: filter params
    """
    instance = models.Institution.objects.get(pk=pk)

    periods_query = models.Period.objects.prefetch_related(
        "positions",
        "positions__person",
    ).filter(
        institution=instance,
        positions__person__birth_date__isnull=False,
    )

    has_query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        birth_date__isnull=False,
    )

    none_query = models.Period.objects.prefetch_related(
        "positions",
        "positions__person",
    ).filter(
        institution=instance,
        positions__person__birth_date__isnull=True,
    )

    if params.get("genre"):
        periods_query = periods_query.filter(
            positions__person__genre=params.get("genre")
        )
        has_query = none_query.filter(genre=params.get("genre"))
        none_query = none_query.filter(positions__person__genre=params.get("genre"))

    periods_query = periods_query.values("id", "name", "start", "end").annotate(
        mean_age=Avg(F("positions__start") - F("positions__person__birth_date"))
    )

    if params.get("split") and params.get("split") == "genre":
        periods_query = periods_query.annotate(genre=F("positions__person__genre"))

    periods_query = periods_query.order_by("id")

    return {
        "instance": serializers.InstitutionRetrieveSerializer(instance).data,
        "periods": serializers.InstitutionMeanAgeSerializer(
            periods_query,
            many=True,
        ).data,
        "has_date": has_query.count(),
        "no_date": none_query.count(),
    }
