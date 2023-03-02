# -*- coding: utf-8 -*-
from django_filters import CharFilter, rest_framework as rf_filters
from positions.models import Position


class PositionFilter(rf_filters.FilterSet):
    class Meta:
        model = Position
        fields = (
            "full_name",
            "short_name",
            "person",
            "period",
            "start",
            "end",
        )
