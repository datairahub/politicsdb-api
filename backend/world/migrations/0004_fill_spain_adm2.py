# -*- coding: utf-8 -*-
from django.db import migrations

spain_adm2 = [
    ["es_clm", "es_alb", "02", "Albacete"],
    ["es_val", "es_ali", "03", "Alicante"],
    ["es_and", "es_alm", "04", "Almería"],
    ["es_vas", "es_ara", "01", "Araba"],
    ["es_ast", "es_ast", "33", "Asturias"],
    ["es_cyl", "es_avi", "05", "Ávila"],
    ["es_ext", "es_bad", "06", "Badajoz"],
    ["es_iba", "es_iba", "07", "Illes Balears"],
    ["es_cat", "es_bar", "08", "Barcelona"],
    ["es_vas", "es_biz", "48", "Bizkaia"],
    ["es_cyl", "es_bur", "09", "Burgos"],
    ["es_ext", "es_cac", "10", "Cáceres"],
    ["es_and", "es_cad", "11", "Cádiz"],
    ["es_can", "es_can", "39", "Cantabria"],
    ["es_val", "es_cas", "12", "Castellón"],
    ["es_clm", "es_ciu", "13", "Ciudad Real"],
    ["es_and", "es_cor", "14", "Córdoba"],
    ["es_gal", "es_aco", "15", "A Coruña"],
    ["es_clm", "es_cue", "16", "Cuenca"],
    ["es_vas", "es_gip", "20", "Gipuzkoa"],
    ["es_cat", "es_gir", "17", "Girona"],
    ["es_and", "es_gra", "18", "Granada"],
    ["es_clm", "es_gua", "19", "Guadalajara"],
    ["es_and", "es_hue", "21", "Huelva"],
    ["es_ara", "es_hus", "22", "Huesca"],
    ["es_and", "es_jae", "23", "Jaén"],
    ["es_cyl", "es_leo", "24", "León"],
    ["es_cat", "es_lle", "25", "Lleida"],
    ["es_cyl", "es_lug", "27", "Lugo"],
    ["es_mad", "es_mad", "28", "Madrid"],
    ["es_and", "es_mal", "29", "Málaga"],
    ["es_mur", "es_mur", "30", "Murcia"],
    ["es_nav", "es_nav", "31", "Navarra"],
    ["es_gal", "es_our", "32", "Ourense"],
    ["es_cyl", "es_pal", "34", "Palencia"],
    ["es_ica", "es_lpa", "35", "Las Palmas"],
    ["es_gal", "es_pon", "36", "Pontevedra"],
    ["es_rio", "es_rio", "26", "La Rioja"],
    ["es_cyl", "es_sal", "37", "Salamanca"],
    ["es_ica", "es_sct", "38", "Santa Cruz de Tenerife"],
    ["es_cyl", "es_seg", "40", "Segovia"],
    ["es_and", "es_sev", "41", "Sevilla"],
    ["es_cyl", "es_sor", "42", "Soria"],
    ["es_cat", "es_tar", "43", "Tarragona"],
    ["es_ara", "es_ter", "44", "Teruel"],
    ["es_clm", "es_tol", "45", "Toledo"],
    ["es_val", "es_val", "46", "Valencia"],
    ["es_cyl", "es_vad", "47", "Valladolid"],
    ["es_cyl", "es_zam", "49", "Zamora"],
    ["es_ara", "es_zar", "50", "Zaragoza"],
    ["es_ceu", "es_ceu", "51", "Ceuta"],
    ["es_mel", "es_mel", "52", "Melilla"],
]


def apply_migration(apps, schema_editor):
    spain = apps.get_model("world", "Adm0").objects.get(code="es")
    Adm1 = apps.get_model("world", "Adm1")
    Adm2 = apps.get_model("world", "Adm2")

    for row in spain_adm2:
        Adm2(
            name=row[3],
            code=row[1],
            adm0=spain,
            adm1=Adm1.objects.get(code=row[0]),
            metadata={"ine_code": row[2]},
        ).save()


def revert_migration(apps, schema_editor):
    apps.get_model("world", "Adm2").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0003_fill_spain_adm1"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
