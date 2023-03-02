# -*- coding: utf-8 -*-
from rest_framework import serializers

from positions.models import Position


class PositionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "id",
            "short_name",
            "full_name",
            "person",
            "period",
            "start",
            "end",
        )


class PositionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = (
            "id",
            "short_name",
            "full_name",
            "person",
            "period",
            "start",
            "end",
        )
