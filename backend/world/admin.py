# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from .models import (
    Adm0,
    Adm1,
    Adm2,
    Adm3,
    Adm4,
)


class Adm0Admin(BaseAdmin):
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
