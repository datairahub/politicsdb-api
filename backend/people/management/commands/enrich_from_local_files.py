# -*- coding: utf-8 -*-
import os
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from people.models import Person
from people.services.birth_dates import register_birth_date_source

logger = logging.getLogger("commands")


class Command(BaseCommand):
    help = "Update data using local files"
    data_folder = settings.BASE_DIR.parent / "data_input" / "birth_dates"

    def handle(self, *args, **options):
        for filename in self.get_data_files():
            self.update_birth_dates_from_file(filename, *args, **options)

        if options["verbosity"] >= 2:
            logger.info("Done")

    def get_data_files(self):
        return [
            str(file)
            for file in os.listdir(self.data_folder)
            if str(file).endswith(".csv")
        ]

    def update_birth_dates_from_file(self, filename, *args, **options):
        with open(self.data_folder / filename, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            for row in csv_reader:
                if not row.get("source") or not row.get("birth_date"):
                    continue

                if not row.get("full_name") and not (
                    row.get("first_name") and row.get("last_name")
                ):
                    continue

                full_name = row.get(
                    "full_name", f"{row.get('first_name')} {row.get('last_name')}"
                )
                person = Person.objects.filter(full_name=full_name).first()

                if not person:
                    logger.warn(f"{full_name}: NOT FOUND")
                    continue

                register_birth_date_source(
                    person=person,
                    url=row["source"],
                    value=row["birth_date"],
                )

                if options["verbosity"] >= 2:
                    logger.info(f"{person}")
