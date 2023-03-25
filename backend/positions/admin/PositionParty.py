# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from positions.models import PositionParty


class PositionPartyAdmin(BaseMetadataAdmin):
    model = PositionParty
    list_display = (
        "position",
        "party",
        "start",
        "end",
    )
    # search_fields = ("name",)
    # ordering = ("name",)
    # list_filter = (
    #     "institution",
    #     "start",
    #     "end",
    # )


admin.site.register(PositionParty, PositionPartyAdmin)
