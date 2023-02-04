# -*- coding: utf-8 -*-
from django.db import migrations

DATA = [
    ["1979-04-03", "1983-05-08"],
    ["1983-05-08", "1987-06-10"],
    ["1987-06-10", "1991-05-26"],
    ["1991-05-26", "1995-05-28"],
    ["1995-05-28", "1999-06-13"],
    ["1999-06-13", "2003-05-25"],
    ["2003-05-25", "2007-05-27"],
    ["2007-05-27", "2011-05-22"],
    ["2011-05-22", "2015-05-24"],
    ["2015-05-24", "2019-05-26"],
    ["2019-05-26", "2023-05-28"],
]


def apply_migration(apps, schema_editor):
    CityCouncilTerm = apps.get_model("governors", "CityCouncilTerm")
    spain = apps.get_model("world", "Adm0").objects.get(code="es")

    for row in DATA:
        CityCouncilTerm(adm0=spain, date_start=row[0], date_end=row[1]).save()


def revert_migration(apps, schema_editor):
    CityCouncilTerm = apps.get_model("governors", "CityCouncilTerm")
    CityCouncilTerm.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("governors", "0006_fill_spain_governors"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
