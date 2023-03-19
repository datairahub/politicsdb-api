# -*- coding: utf-8 -*-
from django.db.models import F, Avg, Count

from core.cache import cached_stats
from people.models import Person
from positions.models import (
    Institution,
    Period,
)
from positions.serializers import (
    InstitutionRetrieveSerializer,
    InstitutionDistributionAgeSerializer,
    InstitutionMeanAgeSerializer,
    InstitutionGenreSerializer,
)


@cached_stats(base="INSTITUTION_DISTRIBUTION_AGE")
def get_institution_distribution_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution distribution age stats

    :param pk: institution primary key
    :param params: filter params
    """
    instance = Institution.objects.get(pk=pk)
    person_query = Person.objects.prefetch_related(
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
        person_query = person_query.filter(genre=params.get("genre"))
        none_query = none_query.filter(genre=params.get("genre"))

    person_query = person_query.annotate(
        position_start=F("positions__start"),
        position_end=F("positions__end"),
    )

    return {
        "instance": InstitutionRetrieveSerializer(instance).data,
        "persons": InstitutionDistributionAgeSerializer(person_query, many=True).data,
        "no_date": none_query.count(),
    }


@cached_stats(base="INSTITUTION_MEAN_AGE")
def get_institution_mean_age_stats(pk: str, params: dict) -> dict:
    """
    Return institution mean age stats

    :param pk: institution primary key
    :param params: filter params
    """
    instance = Institution.objects.get(pk=pk)

    periods_query = Period.objects.prefetch_related(
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

    none_query = Period.objects.prefetch_related(
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
        "instance": InstitutionRetrieveSerializer(instance).data,
        "periods": InstitutionMeanAgeSerializer(periods_query, many=True).data,
        "has_date": has_query.count(),
        "no_date": none_query.count(),
    }


def get_institution_genre_stats(pk: str, params: dict) -> dict:
    """
    Return institution genre stats

    :param pk: institution primary key
    :param params: filter params
    """
    instance = Institution.objects.get(pk=pk)

    periods_query = (
        Period.objects.prefetch_related(
            "positions",
            "positions__person",
        )
        .filter(
            institution=instance,
        )
        .annotate(genre=F("positions__person__genre"))
        .values("id", "name", "start", "end", "genre")
        .annotate(total=Count("genre"))
        .order_by("id")
    )

    has_query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        genre__isnull=False,
    )

    none_query = Person.objects.prefetch_related(
        "positions",
        "positions__period",
        "positions__period__institution",
    ).filter(
        positions__period__institution_id=pk,
        genre__isnull=True,
    )

    return {
        "instance": InstitutionRetrieveSerializer(instance).data,
        "periods": InstitutionGenreSerializer(periods_query, many=True).data,
        "has_genre": has_query.count(),
        "no_genre": none_query.count(),
    }
