# -*- coding: utf-8 -*-
import csv
import logging
from django.conf import settings
from django.core.management.base import BaseCommand

from people.services.people_id import people_id_from_name
from people.services.names import clean_spanish_name
from people.services.birth_dates import register_birth_date_source
from positions.models import (
    Position,
    Period,
)
from people.models import (
    Person,
)
from organizations.models import (
    Candidacy,
)

logger = logging.getLogger("commands")


class Command(BaseCommand):
    """
    Get or update spanish goverment positions from the
    source file. The following data are obtained:

    Position:
    - short_name, full_name
    - person
    - period
    - start, end
    - candidacy
    """

    help = "Update Spain goverment positions"
    file = settings.BASE_DIR.parent / "data_input" / "positions" / "es_governors.csv"

    def handle(self, *args, **options):
        with open(self.file, "r") as f:
            csv_reader = csv.DictReader(f, delimiter=",")

            for row in csv_reader:

                person = Person.objects.filter(
                    id_name=people_id_from_name(row.get("person_name"))
                ).first()
                if not person:
                    person = Person(full_name=row.get("person_name"), genre="O")
                    person.save()

                period = Period.objects.get(name=row.get("period_name"))
                candidacy = Candidacy.objects.get(
                    short_name=row.get("candidacy"),
                    period__number=int(row["legislature"]),
                )

                position = Position(
                    short_name=row.get("position_short_name"),
                    full_name=row.get("position_full_name"),
                    person=person,
                    period=period,
                    start=row.get("start"),
                    end=row.get("end"),
                    candidacy=candidacy,
                )
                position.save()

                if options["verbosity"] >= 2:
                    logger.info(f"{position}")
