# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from people.models import BirthDateSource


class BirthDateSourceAdmin(BaseAdmin):
    model = BirthDateSource
    list_display = (
        "person",
        "name",
        "value",
    )
    ordering = ("date",)
    list_filter = (
        "date",
        "accuracy",
    )
    search_fields = ("person__full_name", "value")
    readonly_fields = ("person",)
    exclude = ("name", "date", "accuracy")


admin.site.register(BirthDateSource, BirthDateSourceAdmin)
