# -*- coding: utf-8 -*-
from django.db import migrations


def apply_migration(apps, schema_editor):
    Adm0 = apps.get_model("world", "Adm0")
    Adm0(name="España", iso_name="Spain", code="es").save()


def revert_migration(apps, schema_editor):
    Adm0 = apps.get_model("world", "Adm0")
    Adm0.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
