# -*- coding: utf-8 -*-
import csv
import json
from django.contrib import admin
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe
from django.http import HttpResponse


class BaseAdmin(admin.ModelAdmin):
    readonly_fields = ("pretty_metadata",)
    exclude = ("metadata",)
    actions = ("download_csv",)

    # def has_add_permission(self, request, obj=None):
    #     return False

    # def has_delete_permission(self, request, obj=None):
    #     return False

    # def has_change_permission(self, request, obj=None):
    #     return True

    def pretty_metadata(self, instance):
        """Function to display pretty version of our data"""

        # Convert the data to sorted, indented JSON
        response = json.dumps(instance.metadata, sort_keys=True, indent=2)

        # Truncate the data. Alter as needed
        # response = response[:5000]

        # Get the Pygments formatter
        formatter = HtmlFormatter(style="colorful")

        # Highlight the data
        response = highlight(response, JsonLexer(), formatter)

        # Get the stylesheet
        style = "<style>" + formatter.get_style_defs() + "</style><br>"

        # Safe the output
        return mark_safe(style + response)  # nosec

    pretty_metadata.short_description = "Metadata"

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


class ReadOnlyInline(admin.TabularInline):
    extra = 0
    show_change_link = True

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
