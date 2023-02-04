# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin, ReadOnlyInline
from positions.models import Institution, Period


class PeriodInline(ReadOnlyInline):
    model = Period
    fields = ("name", "code", "number", "start", "end")


class InstitutionAdmin(BaseAdmin):
    model = Institution
    list_display = (
        "name",
        "adm0",
        "adm1",
        "adm2",
        "adm3",
        "adm4",
    )
    search_fields = ("name",)
    ordering = ("name",)
    readonly_fields = (
        "adm0",
        "adm1",
        "adm2",
        "adm3",
        "adm4",
    )
    inlines = (PeriodInline,)


admin.site.register(Institution, InstitutionAdmin)
