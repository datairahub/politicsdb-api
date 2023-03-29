# -*- coding: utf-8 -*-
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from positions.models import (
    Institution,
)
from world.models import (
    Adm0,
    Adm1,
    Adm2,
    Adm3,
    Adm4,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Get or update institutions. The following data
    are obtained:

    Institution:
    - name
    - adm0, adm1, adm2, adm3, adm4
    """

    help = "Update institutions"
    file = settings.BASE_DIR.parent / "data_input" / "institutions" / "institutions.csv"

    def handle(self, *args, **options):
        with open(self.file, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")

            for row in csv_reader:
                institution = Institution.objects.filter(
                    name=row["name"],
                ).first()

                if not institution:
                    institution = Institution(
                        name=row["name"],
                    )

                institution.adm0 = (
                    Adm0.objects.filter(code=row["adm0"]).first()
                    if row.get("adm0")
                    else None
                )
                institution.adm1 = (
                    Adm1.objects.filter(code=row["adm1"]).first()
                    if row.get("adm1")
                    else None
                )
                institution.adm2 = (
                    Adm2.objects.filter(code=row["adm2"]).first()
                    if row.get("adm2")
                    else None
                )
                institution.adm3 = (
                    Adm3.objects.filter(code=row["adm3"]).first()
                    if row.get("adm3")
                    else None
                )
                institution.adm4 = (
                    Adm4.objects.filter(code=row["adm4"]).first()
                    if row.get("adm4")
                    else None
                )
                institution.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{institution}")
