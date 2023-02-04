# -*- coding: utf-8 -*-
import re
import csv
from pathlib import Path
from unidecode import unidecode
from django.db import migrations
from django.conf import settings

INE_FILE = (
    Path(settings.BASE_DIR).parent
    / "data_input"
    / "locations"
    / "spain_adm2_adm3_adm4.csv"
)


def get_adm2_code_from_name(name):
    adm2s = {
        "Alava": "es_ara",
        "Albacete": "es_alb",
        "Alicante": "es_ali",
        "Almería": "es_alm",
        "Avila": "es_avi",
        "Badajoz": "es_bad",
        "Illes Balears": "es_iba",
        "Barcelona": "es_bar",
        "Burgos": "es_bur",
        "Cáceres": "es_cac",
        "Cádiz": "es_cad",
        "Castellón de la Plana": "es_cas",
        "Ciudad Real": "es_ciu",
        "Córdoba": "es_cor",
        "A Coruña": "es_aco",
        "Cuenca": "es_cue",
        "Girona": "es_gir",
        "Granada": "es_gra",
        "Guadalajara": "es_gua",
        "Guipúzcoa": "es_gip",
        "Huelva": "es_hue",
        "Huesca": "es_hus",
        "Jaén": "es_jae",
        "León": "es_leo",
        "Lleida": "es_lle",
        "La Rioja": "es_rio",
        "Lugo": "es_lug",
        "Madrid": "es_mad",
        "Málaga": "es_mal",
        "Murcia": "es_mur",
        "Navarra": "es_nav",
        "Ourense": "es_our",
        "Asturias": "es_ast",
        "Palencia": "es_pal",
        "Las Palmas": "es_lpa",
        "Pontevedra": "es_pon",
        "Salamanca": "es_sal",
        "Santa Cruz de Tenerife": "es_sct",
        "Cantabria": "es_can",
        "Segovia": "es_seg",
        "Sevilla": "es_sev",
        "Soria": "es_sor",
        "Tarragona": "es_tar",
        "Teruel": "es_ter",
        "Toledo": "es_tol",
        "Valencia": "es_val",
        "Valladolid": "es_vad",
        "Vizcaya": "es_biz",
        "Zamora": "es_zam",
        "Zaragoza": "es_zar",
    }
    return adm2s.get(name)


def apply_migration(apps, schema_editor):
    spain = apps.get_model("world", "Adm0").objects.get(code="es")
    Adm2 = apps.get_model("world", "Adm2")
    Adm3 = apps.get_model("world", "Adm3")
    Adm4 = apps.get_model("world", "Adm4")
    hp_pattern = re.compile(r"[\W_]+")

    with open(INE_FILE) as csv_file:
        adm2 = None
        adm3 = None
        reader = csv.reader(csv_file, delimiter=",")
        next(reader)
        for row in reader:
            if (not row[0]) and (not row[1]):
                continue

            if row[0]:
                # New Adm2 starts
                adm2 = Adm2.objects.get(code=get_adm2_code_from_name(row[0]))

            if row[1].startswith("Comarca"):
                # New Adm3 starts
                splited = row[1].split(":")
                adm3_name = splited[1].strip()
                adm3_ine = splited[0].split(" ")[-1]
                adm3_code = (
                    adm2.code + "_" + hp_pattern.sub("", unidecode(adm3_name).lower())
                )
                adm3 = Adm3(
                    name=adm3_name,
                    code=adm3_code,
                    adm0=spain,
                    adm1=adm2.adm1,
                    adm2=adm2,
                    metadata={"ine_code": adm3_ine},
                )
                adm3.save()
            elif row[1] and row[2]:
                # New Adm4 starts
                adm4_ine = row[1]
                adm4_name = row[2]
                adm4_code = (
                    adm2.code + "_" + hp_pattern.sub("", unidecode(adm4_name).lower())
                )
                Adm4(
                    name=adm4_name,
                    code=adm4_code,
                    adm0=spain,
                    adm1=adm2.adm1,
                    adm2=adm2,
                    adm3=adm3,
                    metadata={"ine_code": adm4_ine},
                ).save()


def revert_migration(apps, schema_editor):
    apps.get_model("world", "Adm3").objects.all().delete()
    apps.get_model("world", "Adm4").objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ("world", "0004_fill_spain_adm2"),
    ]

    operations = [
        migrations.RunPython(apply_migration, revert_migration),
    ]
