# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from positions.models import Position


class PositionAdmin(BaseMetadataAdmin):
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
    autocomplete_fields = ("person", "period")

    def get_readonly_fields(self, request, obj=None):
        return (
            (
                "person",
                "period",
            )
            if obj
            else tuple()
        )


admin.site.register(Position, PositionAdmin)
