# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from positions.models import Period


class PeriodAdmin(BaseAdmin):
    model = Period
    list_display = (
        "name",
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
    date_hierarchy = "start"


admin.site.register(Period, PeriodAdmin)
