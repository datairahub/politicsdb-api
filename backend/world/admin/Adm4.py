# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from world.models import Adm4


class Adm4Admin(BaseMetadataAdmin):
    model = Adm4
    list_display = (
        "name",
        "code",
        "adm3",
        "adm2",
        "adm1",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)
    readonly_fields = BaseMetadataAdmin.readonly_fields + (
        "adm0",
        "adm1",
        "adm2",
        "adm3",
    )


admin.site.register(Adm4, Adm4Admin)
