# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from world.models import Adm1


class Adm1Admin(BaseMetadataAdmin):
    model = Adm1
    list_display = (
        "name",
        "code",
        "adm0",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)
    readonly_fields = BaseMetadataAdmin.readonly_fields + ("adm0",)


admin.site.register(Adm1, Adm1Admin)
