# -*- coding: utf-8 -*-
import csv
import json
from django.contrib.gis import admin
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from django.http import HttpResponse


class BaseAdmin(admin.OSMGeoAdmin):
    actions = ("download_csv",)

    def download_csv(modeladmin, request, queryset):
        opts = queryset.model._meta
        # model = queryset.model
        response = HttpResponse(content_type="text/csv")
        # force download.
        response[
            "Content-Disposition"
        ] = f"attachment;filename={queryset.model.__name__}.csv"
        # the csv writer
        writer = csv.writer(response)
        field_names = [
            field.name for field in opts.fields if not field.name == "metadata"
        ]
        # Write a first row with header information
        writer.writerow(field_names)
        # Write data rows
        for obj in queryset:
            row = []
            for field in field_names:
                row.append(
                    getattr(obj, "person").id_name
                ) if field == "person" else row.append(getattr(obj, field))
            writer.writerow(row)
        return response

    download_csv.short_description = "Download selected as csv"


class BaseMetadataAdmin(BaseAdmin):
    readonly_fields = ("pretty_metadata",)
    exclude = ("metadata",)

    def pretty_metadata(self, instance):
        """Function to display pretty version of our data"""

        response = json.dumps(instance.metadata, sort_keys=True, indent=2)
        formatter = HtmlFormatter(style="colorful")
        response = highlight(response, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + response)  # nosec

    pretty_metadata.short_description = "Metadata"


class DateSourceAdmin(BaseAdmin):
    list_display = (
        "person",
        "name",
        "value",
    )
    ordering = ("date",)
    list_filter = (
        "date",
        "accuracy",
    )
    autocomplete_fields = ("person",)
    search_fields = ("person__full_name", "value")
    exclude = (
        "name",
        "date",
        "pretty_metadata",
    )

    def get_readonly_fields(self, request, obj=None):
        return (
            (
                "person",
                "accuracy",
            )
            if obj
            else ("accuracy",)
        )


class ReadOnlyInline(admin.TabularInline):
    extra = 0
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
