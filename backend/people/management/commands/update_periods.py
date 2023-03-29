# -*- coding: utf-8 -*-
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from positions.models import (
    Institution,
    Period,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Get or update periods. The following data
    are obtained:

    Period:
    - institution
    - number
    - name         # Always updated
    - start        # Always updated
    - end          # Always updated
    - code         # Always updated
    """

    help = "Update periods"
    file = settings.BASE_DIR.parent / "data_input" / "periods" / "periods.csv"

    def handle(self, *args, **options):
        with open(self.file, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")

            for row in csv_reader:
                institution = Institution.objects.get(name=row["institution"])

                period = Period.objects.filter(
                    institution=institution,
                    number=int(row["number"]),
                ).first()

                if not period:
                    period = Period(
                        institution=institution,
                        number=int(row["number"]),
                    )

                period.name = row["name"]
                period.code = row["code"]
                period.start = row["start"]
                period.end = row["end"]

                period.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{period}")
