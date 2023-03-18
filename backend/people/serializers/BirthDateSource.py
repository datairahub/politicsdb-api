# -*- coding: utf-8 -*-
from rest_framework import serializers

from people.models import BirthDateSource


class BirthDateSourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BirthDateSource
        fields = (
            "id",
            "person",
            "name",
            "url",
            "value",
            "date",
            "accuracy",
        )
