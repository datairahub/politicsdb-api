# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from people.models import BirthSource


class BirthSourceAdmin(BaseAdmin):
    model = BirthSource
    list_display = (
        "person",
        "name",
        "url",
        "is_exact",
        "date",
    )
    ordering = ("date",)
    list_filter = (
        "is_exact",
        "date",
    )
    date_hierarchy = "date"
    readonly_fields = ("person",)


admin.site.register(BirthSource, BirthSourceAdmin)
