# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from world.models import Adm4


class Adm4Admin(BaseAdmin):
    model = Adm4
    list_display = (
        "name",
        "adm3",
        "adm2",
        "adm1",
        "code",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)


admin.site.register(Adm4, Adm4Admin)
