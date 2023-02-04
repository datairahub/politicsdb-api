# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from world.models import Adm3


class Adm3Admin(BaseAdmin):
    model = Adm3
    list_display = (
        "name",
        "adm2",
        "adm1",
        "code",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)


admin.site.register(Adm3, Adm3Admin)
