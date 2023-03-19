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
    autocomplete_fields = ("person",)
    exclude = ("name", "pretty_metadata")

    def get_readonly_fields(self, request, obj=None):
        return ("person",) if obj else tuple()


admin.site.register(BiographySource, BiographySourceAdmin)
