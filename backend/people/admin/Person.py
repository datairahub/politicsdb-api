# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin, ReadOnlyInline
from people.models import (
    Person,
    BirthDateSource,
    BiographySource,
)


class BirthDateSourceInline(ReadOnlyInline):
    model = BirthDateSource
    fields = ("value", "url")


class BiographySourceInline(ReadOnlyInline):
    model = BiographySource
    fields = ("value", "url")


class PersonAdmin(BaseMetadataAdmin):
    model = Person
    list_display = (
        "full_name",
        "id_name",
        "birth_date",
        "genre",
    )
    search_fields = ("full_name", "id_name")
    ordering = ("full_name",)
    list_filter = (
        "birth_date",
        "birth_date_accuracy",
        "death_date",
        "genre",
    )
    readonly_fields = BaseMetadataAdmin.readonly_fields + (
        "id_name",
        "birth_date",
        "birth_date_accuracy",
    )
    exclude = BaseMetadataAdmin.exclude + (
        "birth_place",
        "birth_place_name",
        "death_date",
        "death_date_accuracy",
        "death_place",
        "death_place_name",
    )
    inlines = (
        BirthDateSourceInline,
        BiographySourceInline,
    )


admin.site.register(Person, PersonAdmin)
