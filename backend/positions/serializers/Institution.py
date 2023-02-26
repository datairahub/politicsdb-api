# -*- coding: utf-8 -*-
from rest_framework import serializers

from positions.models import Institution


class InstitutionSerializer(serializers.ModelSerializer):
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
