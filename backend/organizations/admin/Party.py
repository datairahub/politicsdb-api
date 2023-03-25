# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from organizations.models import Party


class PartyAdmin(BaseMetadataAdmin):
    model = Party
    list_display = (
        "name",
        "short_name",
        "color",
        "adm0",
    )
    search_fields = ("name", "short_name")
    ordering = ("name",)
    autocomplete_fields = ("adm0",)


admin.site.register(Party, PartyAdmin)
