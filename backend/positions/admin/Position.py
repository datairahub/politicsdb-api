# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from positions.models import Position


class PositionAdmin(BaseAdmin):
    model = Position
    list_display = (
        "full_name",
        "person",
        "period",
        "start",
        "end",
    )
    search_fields = ("short_name", "full_name")
    ordering = ("short_name",)
    list_filter = (
        "start",
        "end",
    )
    readonly_fields = ("person",)


admin.site.register(Position, PositionAdmin)
