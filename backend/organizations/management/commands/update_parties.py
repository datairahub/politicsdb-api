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
    data_input/parties/spain_parties.csv
    """

    help = "Update Parties"
    data = settings.BASE_DIR.parent / "data_input" / "parties" / "adm0_parties.csv"

    def handle(self, *args, **options):
        with open(self.data, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row in reader:
                adm0 = Adm0.objects.get(code=row["adm0"].lower())
                party = Party.objects.filter(
                    short_name=row["short_name"],
                    adm0=adm0,
                ).first()

                if not party:
                    party = Party.objects.create(
                        short_name=row["short_name"],
                        adm0=adm0,
                        name=row["name"],
                        color=row["color"],
                    )
                else:
                    party.name = row["name"]
                    party.color = row["color"]
                    party.save()

        logger.info(f"Parties update done")
