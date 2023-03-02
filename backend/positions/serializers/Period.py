# -*- coding: utf-8 -*-
from rest_framework import serializers

from positions.models import Period


class PeriodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = (
            "id",
            "name",
            "number",
            "code",
            "institution",
            "start",
            "end",
        )


class PeriodRetrieveSerializer(serializers.ModelSerializer):
    institution_name = serializers.SerializerMethodField()

    def get_institution_name(self, obj):
        return obj.institution.name

    class Meta:
        model = Period
        fields = (
            "id",
            "name",
            "number",
            "code",
            "institution",
            "institution_name",
            "start",
            "end",
        )
