# -*- coding: utf-8 -*-
from django.db.models import Q
from django_filters import CharFilter, rest_framework as rf_filters
from people.models import Person
from people.services.people_id import people_id_from_name


class PersonFilter(rf_filters.FilterSet):
    search = CharFilter(method="filter_search")
    period = CharFilter(method="filter_period")
    institution = CharFilter(method="filter_institution")
    birth_date__isnull = CharFilter(method="filter_birth_date__isnull")

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(full_name__icontains=value)
            | Q(id_name__icontains=people_id_from_name(value))
        )

    def filter_period(self, queryset, name, value):
        return (
            queryset.prefetch_related(
                "positions",
                "positions__period",
            )
            .filter(positions__period=value)
            .distinct()
        )

    def filter_institution(self, queryset, name, value):
        return (
            queryset.prefetch_related(
                "positions",
                "positions__period",
                "positions__period__institution",
            )
            .filter(positions__period__institution=value)
            .distinct()
        )
    
    def filter_birth_date__isnull(self, queryset, name, value):
        if value == "true":
            return queryset.filter(birth_date__isnull=True)
        if value == "false":
            return queryset.filter(birth_date__isnull=False)
        return queryset

    class Meta:
        model = Person
        fields = (
            "full_name",
            "first_name",
            "last_name",
            "genre",
            "period",
            "institution",
            "birth_date__isnull",
        )
