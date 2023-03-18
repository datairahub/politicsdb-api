# -*- coding: utf-8 -*-
from rest_framework import serializers

from people.models import BiographySource


class BiographySourceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BiographySource
        fields = (
            "id",
            "person",
            "name",
            "url",
            "value",
        )
