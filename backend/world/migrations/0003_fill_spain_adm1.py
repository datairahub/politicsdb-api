# -*- coding: utf-8 -*-
from django.db import migrations

spain_adm1 = [
    ["es_and", "01", "Andalucía"],
    ["es_ara", "02", "Aragón"],
    ["es_ast", "03", "Principado de Asturias"],
    ["es_iba", "04", "Illes Balears"],
    ["es_ica", "05", "Canarias"],
    ["es_can", "06", "Cantabria"],
    ["es_cyl", "07", "Castilla y León"],
    ["es_clm", "08", "Castilla - La Mancha"],
    ["es_cat", "09", "Cataluña"],
    ["es_val", "10", "Comunitat Valenciana"],
    ["es_ext", "11", "Extremadura"],
    ["es_gal", "12", "Galicia"],
    ["es_mad", "13", "Comunidad de Madrid"],
    ["es_mur", "14", "Región de Murcia"],
    ["es_nav", "15", "Comunidad Foral de Navarra"],
    ["es_vas", "16", "País Vasco"],
    ["es_rio", "17", "La Rioja"],
    ["es_ceu", "18", "Ceuta"],
    ["es_mel", "19", "Melilla"],
]


def apply_migration(apps, schema_editor):
    spain = apps.get_model("world", "Adm0").objects.get(code="es")
    Adm1 = apps.get_model("world", "Adm1")

    for row in spain_adm1:
        Adm1(
            name=row[2],
            code=row[0],
            adm0=spain,
            metadata={"ine_code": row[1]},
        ).save()


def revert_migration(apps, schema_editor):
    apps.get_model("world", "Adm1").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0002_fill_spain_adm0"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
