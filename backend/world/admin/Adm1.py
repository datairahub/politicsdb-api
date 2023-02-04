# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from world.models import Adm1


class Adm1Admin(BaseAdmin):
    model = Adm1
    list_display = (
        "name",
        "adm0",
        "code",
    )
    search_fields = (
        "name",
        "code",
    )
    ordering = ("name",)


admin.site.register(Adm1, Adm1Admin)
