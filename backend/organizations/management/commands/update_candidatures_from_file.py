# -*- coding: utf-8 -*-
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand
from organizations.models import Party, Candidacy, PartyCandidacy
from positions.models import Period

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Create or update spanish candidatures from
    local file. The following data is fetched:

    Candidacy
    - short_name
    - name              # Always updated
    - period            # Always updated
    - political_space   # Always updated
    - source            # Always updated
    """

    help = "Update candidatures"
    data = settings.BASE_DIR.parent / "data_input" / "candidacies" / "es_congress.csv"

    def handle(self, *args, **options):
        with open(self.data, "r") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",", quotechar='"')
            for row in reader:
                period = Period.objects.get(
                    number=int(row["legislature"]),
                    institution__name="Parlamento de España",
                )
                candidacy = Candidacy.objects.filter(
                    period=period, short_name=row["short_name"]
                ).first()

                if not candidacy:
                    candidacy = Candidacy(
                        period=period,
                        short_name=row["short_name"],
                    )

                candidacy.name = row["name"]
                candidacy.source = row["source"]
                candidacy.save()

                for party in row["parties_code"].split(","):
                    party = Party.objects.get(code=party)

                    partycandidacy = PartyCandidacy.objects.filter(
                        party=party,
                        candidacy=candidacy,
                    ).first()

                    if not partycandidacy:

                        partycandidacy = PartyCandidacy(
                            party=party,
                            candidacy=candidacy,
                        )

                    partycandidacy.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{candidacy}")
