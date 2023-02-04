# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin, ReadOnlyInline
from positions.models import Period, Position


class PositionInline(ReadOnlyInline):
    model = Position
    fk_name = "period"
    fields = ("full_name", "person")


class PeriodAdmin(BaseAdmin):
    model = Period
    list_display = (
        "__str__",
        "number",
        "code",
        "institution",
        "start",
        "end",
    )
    search_fields = ("name",)
    ordering = ("name",)
    list_filter = (
        "institution",
        "start",
        "end",
    )
    inlines = (PositionInline,)


admin.site.register(Period, PeriodAdmin)
