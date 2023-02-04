# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from world.models import Adm2


class Adm2Admin(BaseAdmin):
    model = Adm2
    list_display = (
        "name",
        "adm1",
        "code",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)


admin.site.register(Adm2, Adm2Admin)
