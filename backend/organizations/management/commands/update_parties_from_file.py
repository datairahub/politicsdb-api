# -*- coding: utf-8 -*-
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from world.models import Adm0
from organizations.models import Party

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Actualizar los partidos políticos en base al archivo
    data_input/parties/adm0_parties.csv
    """

    help = "Update Parties"
    data = settings.BASE_DIR.parent / "data_input" / "parties" / "adm0_es.csv"

    def handle(self, *args, **options):
        adm0 = Adm0.objects.get(code="es")
        with open(self.data, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row in reader:
                party = Party.objects.filter(
                    code=row["code"],
                ).first()

                if not party:
                    party = Party(
                        name=row["name"],
                        adm0=adm0,
                        code=row["code"],
                        start=self.normalize_date(row["start"]),
                        level="adm0",
                    )

                party.founded = self.normalize_date(row["start"])
                party.short_name = row["short_name"]
                party.color = row["color"] or "#000000"
                party.end = self.normalize_date(row["end"])

                party.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{party}")

    def normalize_date(self, str_date: str) -> str:
        if len(str_date) == 7:
            str_date += "-01"
        elif len(str_date) == 4:
            str_date += "-01-01"
        elif len(str_date) == 0:
            str_date = "2999-12-31"

        return str_date
