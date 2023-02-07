# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin, ReadOnlyInline
from people.models import (
    Person,
    BirthDateSource,
    BiographySource,
)


class BirthDateSourceInline(ReadOnlyInline):
    model = BirthDateSource
    fields = ("name", "date", "is_exact", "url")


class BiographySourceInline(ReadOnlyInline):
    model = BiographySource
    fields = ("name", "url", "bio")


class PersonAdmin(BaseAdmin):
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
        "genre",
    )
    date_hierarchy = "birth_date"
    inlines = (
        BirthDateSourceInline,
        BiographySourceInline,
    )


admin.site.register(Person, PersonAdmin)
