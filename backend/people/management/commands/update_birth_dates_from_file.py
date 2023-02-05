# -*- coding: utf-8 -*-
import os
import csv
import logging
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

from people.models import Person
from people.services.birth_dates import register_birth_date_source

logger = logging.getLogger("commands")


class Command(BaseCommand):
    help = "Update birth dates from files"
    data_folder = settings.BASE_DIR.parent / "data_input" / "birth_dates"

    def handle(self, *args, **options):
        for filename in self.get_data_files():
            self.update_birth_dates_from_file(filename)

        logger.info("Done")

    def get_data_files(self):
        return [
            str(file)
            for file in os.listdir(self.data_folder)
            if str(file).endswith(".csv")
        ]

    def update_birth_dates_from_file(self, filename):
        with open(self.data_folder / filename, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")
            for row in csv_reader:
                if not row["source"]:
                    # skip if there is no source
                    continue

                full_name = f"{row['first_name']} {row['last_name']}"
                try:
                    person = Person.objects.get(full_name=full_name)
                except Exception as e:
                    logger.warn(
                        f"Name not found from local birth data file {filename}: {full_name}"
                    )
                    continue

                if not person.metadata.get(filename):
                    person.metadata[filename] = row

                birth_date, is_exact = self.get_birth_date_from_row(row)

                if not birth_date:
                    continue

                if birth_date and birth_date == person.birth_date:
                    # Skip if current date and the new one it's the same
                    continue

                register_birth_date_source(person, row["source"], birth_date, is_exact)

                if person.birth_date and person.birth_date != birth_date and is_exact:
                    # if previous date is set and its not the same, skip
                    logger.warn(
                        f"Different dates for {person}: {person.birth_date} -> {birth_date}"
                    )
                    continue

                person.birth_date = birth_date
                person.save(update_fields=["birth_date"])
                logger.info(f"{person} birth date updated")

    def get_birth_date_from_row(self, row: dict) -> tuple:

        if len(row["birth_date"]) == 4:
            # 1955
            return datetime.strptime(row["birth_date"], "%Y").date(), False

        if len(row["birth_date"]) == 7:
            # 1955-11
            return datetime.strptime(row["birth_date"], "%Y-%m").date(), False

        if len(row["birth_date"]) == 10:
            # 1955-11-06
            return datetime.strptime(row["birth_date"], "%Y-%m-%d").date(), True

        return None
