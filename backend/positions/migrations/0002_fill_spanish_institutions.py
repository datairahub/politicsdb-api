# -*- coding: utf-8 -*-
from django.db import migrations

DATA = [
    "Gobierno de España",
    "Parlamento de España",
    "Senado de España",
]


def apply_migration(apps, schema_editor):
    Institution = apps.get_model("positions", "Institution")
    spain = apps.get_model("world", "Adm0").objects.get(code="es")

    for row in DATA:
        Institution(name=row, adm0=spain).save()


def revert_migration(apps, schema_editor):
    Institution = apps.get_model("positions", "Institution")
    Institution.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("positions", "0001_initial"),
        ("world", "0002_fill_spain_adm0"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
