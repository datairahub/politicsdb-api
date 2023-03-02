# -*- coding: utf-8 -*-
from django_filters import CharFilter, rest_framework as rf_filters
from people.models import Person


class PersonFilter(rf_filters.FilterSet):
    search = CharFilter(method="filter_search")
    period = CharFilter(method="filter_period")
    institution = CharFilter(method="filter_institution")

    def filter_search(self, queryset, name, value):
        return queryset.filter(full_name__icontains=value)

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

    class Meta:
        model = Person
        fields = (
            "full_name",
            "first_name",
            "last_name",
            "genre",
            "period",
            "institution",
        )
