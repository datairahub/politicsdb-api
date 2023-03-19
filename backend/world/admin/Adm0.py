# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseMetadataAdmin
from world.models import Adm0


class Adm0Admin(BaseMetadataAdmin):
    model = Adm0
    list_display = (
        "name",
        "iso_name",
        "code",
    )
    search_fields = (
        "name",
        "iso_name",
        "code",
    )
    ordering = ("name",)


admin.site.register(Adm0, Adm0Admin)
