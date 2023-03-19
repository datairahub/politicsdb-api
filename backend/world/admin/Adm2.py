# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from world.models import Adm2


class Adm2Admin(BaseMetadataAdmin):
    model = Adm2
    list_display = (
        "name",
        "code",
        "adm1",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)
    readonly_fields = BaseMetadataAdmin.readonly_fields + ("adm0", "adm1")


admin.site.register(Adm2, Adm2Admin)
