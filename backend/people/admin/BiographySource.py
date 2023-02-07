# -*- coding: utf-8 -*-
from django.contrib import admin
from core.admins import BaseAdmin
from people.models import BiographySource


class BiographySourceAdmin(BaseAdmin):
    model = BiographySource
    list_display = (
        "person",
        "name",
    )
    readonly_fields = ("person",)


admin.site.register(BiographySource, BiographySourceAdmin)
