# -*- coding: utf-8 -*-
from rest_framework import serializers

from people.models import Person


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = (
            "id",
            "full_name",
            "birth_date",
            "genre",
        )
