# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from persons.models import Person


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


admin.site.register(Person, PersonAdmin)
