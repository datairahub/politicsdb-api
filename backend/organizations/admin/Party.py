# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from organizations.models import Party


class PartyAdmin(BaseAdmin):
    model = Party
    list_display = (
        "short_name",
        "name",
        "color",
        "adm0",
    )
    search_fields = ("name", "short_name")
    ordering = ("name",)
    readonly_fields = ("adm0",)


admin.site.register(Party, PartyAdmin)
