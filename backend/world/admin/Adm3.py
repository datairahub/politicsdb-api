# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from world.models import Adm3


class Adm3Admin(BaseMetadataAdmin):
    model = Adm3
    list_display = (
        "name",
        "code",
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
    )


admin.site.register(Adm3, Adm3Admin)
