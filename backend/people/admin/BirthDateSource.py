# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from people.models import BirthDateSource


class BirthDateSourceAdmin(BaseAdmin):
    model = BirthDateSource
    list_display = (
        "person",
        "name",
        "date",
        "is_exact",
    )
    ordering = ("date",)
    list_filter = (
        "is_exact",
        "date",
    )
    date_hierarchy = "date"
    readonly_fields = ("person",)


admin.site.register(BirthDateSource, BirthDateSourceAdmin)
