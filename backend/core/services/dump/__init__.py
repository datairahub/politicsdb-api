# -*- coding: utf-8 -*-
import csv
import shutil
import logging
from datetime import datetime
from django.conf import settings
from django.apps import apps

logger = logging.getLogger("commands")

DUMPS_DIR = settings.BASE_DIR.parent / "static" / "dump"
DUMPS_TEMP_DIR = DUMPS_DIR / "temp"
LICENSES_DIR = settings.BASE_DIR.parent / "static" / "licenses"
EXCLUDED_APPS = (
    "world",
    "admin",
    "auth",
    "contenttypes",
    "sessions",
)
EXCLUDED_FIELDS = ("metadata",)


def get_dump_info_text():
    export_date = datetime.now()
    return (
        f"Dump date: {export_date}\n"
        "\n"
        "Please refer to the license(s) attached to this file before using it..\n"
        "\n"
        "DATAIRA. Dadasign S.L., VAT-B88334594 (Spain).\n"
    )


def dump_data():
    logger.info("Dump started")

    # Remove previous temporal dump folder
    if DUMPS_TEMP_DIR.exists():
        shutil.rmtree(DUMPS_TEMP_DIR)

    # Create folder
    DUMPS_TEMP_DIR.mkdir(parents=True, exist_ok=True)

    # Dump models
    for model in apps.get_models():
        app_label = model._meta.label.split(".")[0]
        if app_label in EXCLUDED_APPS:
            continue

        field_names = [
            field.name
            for field in model._meta.fields
            if not field.name in EXCLUDED_FIELDS
        ]

        with open(DUMPS_TEMP_DIR / f"{model.__name__}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(field_names)
            for obj in model.objects.all():
                row = []
                for field in field_names:
                    row.append(getattr(obj, field))
                writer.writerow(row)

        logger.info(f"{model.__name__} exported")

    # Copy licenses
    for path in LICENSES_DIR.glob("*"):
        shutil.copyfile(path, DUMPS_TEMP_DIR / path.name)

    # Create readme file
    with open(DUMPS_TEMP_DIR / "INFO.txt", "w") as text_file:
        text_file.write(get_dump_info_text())

    # Compress folder
    shutil.make_archive(DUMPS_DIR / "dump", "zip", DUMPS_TEMP_DIR)

    # Remove previous temporal dump folder
    shutil.rmtree(DUMPS_TEMP_DIR)

    logger.info("Dump done")
