# -*- coding: utf-8 -*-
from rest_framework import serializers

from positions.models import Institution
from positions.serializers.Period import PeriodListSerializer


class InstitutionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            "id",
            "name",
            "adm0",
            "adm1",
            "adm2",
            "adm3",
            "adm4",
        )


class InstitutionRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = (
            "id",
            "name",
            "adm0",
            "adm1",
            "adm2",
            "adm3",
            "adm4",
        )


class InstitutionDistributionAgeSerializer(serializers.Serializer):
    id = serializers.CharField()
    full_name = serializers.CharField()
    genre = serializers.CharField()
    position_start = serializers.DateField()
    position_end = serializers.DateField()
    birth_date = serializers.DateField()


class InstitutionMeanAgeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    start = serializers.DateField()
    end = serializers.DateField()
    mean_seconds = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()

    def get_mean_seconds(self, obj):
        return obj["mean_age"].total_seconds()

    def get_genre(self, obj):
        return obj.get("genre")
